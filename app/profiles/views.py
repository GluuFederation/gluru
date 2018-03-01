import logging
import json
import re
import os
import configparser
from datetime import timedelta
from profiles.gluu_oxd import setup_client
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.decorators.http import require_GET

from social.apps.django_app.default.models import UserSocialAuth

from main.utils import cstm_dates, get_fancy_time, log_error, log_crm, format_minutes

from profiles import constants
from profiles.forms import (
    ProfileForm, RegistrationForm, InvitationForm, NamedRegistrationForm, PartnerForm, OxdConfigurationForm)
from profiles.models import UserProfile, Activation, Invitation, Company, Partnership
from profiles import utils

from tickets.models import Ticket, Answer
from tickets.forms import FilterTicketsForm
from tickets.utils import generate_ticket_link

from connectors.sugarcrm import crm_interface
from connectors.idp import idp_interface


SHA1_RE = re.compile('^[a-f0-9]{40}$')

logger = logging.getLogger('django')


def logout_view(request):

    if request.user:

        try:
            user_social = UserSocialAuth.objects.get(uid=request.user.email)

            try:
                id_token_hint = user_social.extra_data['id_token']

            except TypeError:
                id_token_hint = json.loads(user_social.extra_data)['id_token']

            ox_auth_end_session_url = settings.SOCIAL_AUTH_END_SESSION_ENDPOINT
            post_logout_redirect_uri = settings.SOCIAL_AUTH_POST_LOGOUT_REDIRECT_URL

            logout_url = '{}/?id_token_hint={}&post_logout_redirect_uri={}'.format(
                ox_auth_end_session_url, id_token_hint, post_logout_redirect_uri)

            logout(request)

            return HttpResponseRedirect(logout_url)

        except ObjectDoesNotExist:

            log_error('Logout Failed: Social Auth Credentials for {} could not be found'.format(request.user.email))

        except Exception as e:

            log_error('Logout Failed, Message {}'.format(e.message))

        logout(request)

        return HttpResponseRedirect(reverse('home'))


def register(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':

        registration_form = RegistrationForm(request.POST)

        try:

            if registration_form.is_valid():

                user = registration_form.save(commit=False)
                user.is_active = False
                user.save()

                user.idp_uuid = idp_interface.create_user(
                    user=user, password=registration_form.cleaned_data.get('password1'))

                user.save()

                activation_key = utils.generate_activation_key(user.email)
                activation = Activation(user=user, activation_key=activation_key)
                activation.save()

                utils.send_activation_email(user, activation_key)

                return render(request, 'profiles/registration_complete.html',
                              {'email': user.email})

        except Exception as e:

            logger.exception(e)

            return render(request, 'error.html', {
                'error': 'Registration Failed',
                'description': 'Something went wrong.',
            })

    else:

        registration_form = RegistrationForm()

    return render(request, 'profiles/register.html', {
        'page_type': 'register',
        'registration_form': registration_form})


def register_named(request, activation_key):

    if request.user.is_authenticated():
        logout(request)

    try:
        invitation = Invitation.objects.get(activation_key=activation_key)

    except ObjectDoesNotExist:

        return render(request, 'error.html', {
            'error': 'Invitation Key not recognized',
            'description': 'Sorry, we did not recognize that invitation key. \
                            It either has been used before or is invalid.',
        })

    if request.method == 'POST':

        registration_form = NamedRegistrationForm(
            request.POST,
            email=invitation.email,
            company=invitation.invited_by.company_association.name
        )

        try:

            if registration_form.is_valid():

                user = registration_form.save(commit=False)
                user.save()

                user.idp_uuid = idp_interface.create_user(
                    user=user,
                    password=registration_form.cleaned_data.get('password1'),
                    active=True
                )

                user.crm_type = 'named'
                user.company_association = invitation.invited_by.company_association
                user.company = invitation.invited_by.company_association.name
                user.save()

                invitation.activation_key = 'ACTIVATED'
                invitation.save()

                # crm_interface.upgrade_user_record(user)

                utils.send_new_user_notification(user)

                utils.send_activate_account_notification(user)
                messages.success(request, _('Your account has been activated! You can log in now.'))

                return HttpResponseRedirect(reverse('home'))

        except Exception as e:

            logger.exception(e)

            return render(request, 'error.html', {
                'error': 'Registration Failed',
                'description': 'Something went wrong.',
            })

    else:

        registration_form = NamedRegistrationForm(
            email=invitation.email,
            company=invitation.invited_by.company_association.name
        )

    return render(request, 'profiles/register.html', {'page_type': 'register','registration_form': registration_form})


@require_GET
def activate(request, activation_key):

    if SHA1_RE.search(activation_key):

        try:

            activation = Activation.objects.get(activation_key=activation_key)
            activation.activation_key = 'ACTIVATED'
            activation.save()

            user = activation.user
            user.is_active = True
            user.save()

            # crm_interface.sync_basic_user_with_crm(user)

            if user.is_basic:

                # TODO: move to asynchronous backend task
                utils.notify_company_admin(user)

            idp_interface.activate_user(user)

            utils.send_new_user_notification(user)

            utils.send_activate_account_notification(user)
            messages.success(request, _('Your account has been activated! You can log in now.'))

            return HttpResponseRedirect(reverse('home'))

        except ObjectDoesNotExist as e:

            logger.error('No activation found for {}'.format(activation_key))

        except Exception as e:
            logger.exception(e)

    return render(request, 'error.html', {
        'error': 'Activation Failed',
        'description': 'Sorry, we did not recognize that activation key. \
                        It either has been used before or is invalid.',
    })


@login_required
def add_company_user(request):

    if request.user.crm_type != 'named':

        return HttpResponseRedirect(reverse('home'))

    invitation_form = InvitationForm()

    if request.method == 'POST':

        invitation_form = InvitationForm(request.POST)

        if invitation_form.is_valid():

            email = invitation_form.cleaned_data.get('email')

            try:
                account = UserProfile.objects.get(email=email)

                if not account.is_active:

                    messages.error(request, _('This account has not confirmed their email yet.'))

                elif (account.company_association and
                      account.company_association.name != request.user.company_association.name):

                    messages.error(request, _(
                        'This account is already associated with another company.'))

                else:

                    account.company_association = request.user.company_association
                    account.crm_type = request.user.crm_type
                    account.is_staff = request.user.is_staff
                    account.save()

                    # crm_interface.upgrade_user_record(account)

            except ObjectDoesNotExist:

                try:
                    utils.create_invite(email, request.user)
                    messages.success(request, _('Your invitation has been sent!'))

                except Exception as e:

                    logger.exception(e)
                    messages.error(request, 'Something went wrong. Please contact support@gluu.org')

            return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))

    company_users = request.user.company_association.named_users.all()

    pending_invites = Invitation.objects.filter(invited_by=request.user).exclude(
        activation_key__in=['REVOKED', 'ACTIVATED', 'EXPIRED'])

    support_details = {}

    try:
        support_plan = utils.get_support_details(request)
        if support_plan:
            included_contacts = support_plan['named_contacts']
            remaining_contacts = included_contacts - len(company_users) - len(pending_invites)
            support_details = {
                'support_plan': support_plan['support_plan'],
                'included_contacts': included_contacts,
                'remaining_contacts': remaining_contacts,
                'available_support_time': support_plan['available_support_time'],
                'available_review_time': support_plan['available_review_time'],
                'start_date': support_plan['start_date'],
                'renewal_date': support_plan['renewal_date'],
            }

    except KeyError:

        log_crm('Unexpected support plan value: {}'.format(support_details), 'ERROR')
        pass

    return render(request, 'profiles/my_company.html', {
        'page_type': 'company-users',
        'company_users': company_users,
        'pending_invites': pending_invites,
        'invitation_form': invitation_form,
        'support_details': support_details
    })


@login_required
@require_GET
def add_company_admin(request, user_id):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    try:
        user = UserProfile.objects.get(id=user_id)

        if user.company_association == request.user.company_association:

            user.is_company_admin = True

            # utils.send_account_admin_notification(user)
            utils.send_role_change_notification(user, 'named')

            # crm_interface.update_account_admin_status(user)

            user.save()

        else:

            logger.error('Error Making User Id {} an Account Admin: User does not belong to same company'.format(user_id))

    except ObjectDoesNotExist:

        logger.error('Error Making User Id {} an Account Admin: User not found'.format(user_id))

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))


@login_required
@require_GET
def remove_company_admin(request, user_id):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    try:
        user = UserProfile.objects.get(id=user_id)

        user.is_company_admin = False

        # utils.send_revoke_account_admin_notification(user)
        utils.send_role_change_notification(user, 'admin')

        # crm_interface.update_account_admin_status(user, downgrade=True)

        user.save()

    except ObjectDoesNotExist:

        logger.error('Error Revoking User Id {} as Account Admin: User not found'.format(user_id))

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))


@require_GET
@login_required
def revoke_access(request, user_id):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    try:
        user = UserProfile.objects.get(id=user_id)

        if user.company_association == request.user.company_association:

            user.crm_type = 'user'
            user.is_company_admin = False
            company = user.company_association
            user.company_association = None

            if request.GET.get('deactivate', '') == 'true':

                user.is_active = False
                # utils.send_deactivation_email(user)
                utils.send_role_change_notification(user, 'named', True)

            else:
                # utils.send_revoke_access_email(user, company)
                utils.send_role_change_notification(user, 'named')

            crm_interface.downgrade_named_user(user)

            user.save()

        else:
            log_error('Error Revoking Access of Named Account: User does not belong to same company')

    except ObjectDoesNotExist:

        log_error('Error Revoking Access of Named Account: User not found')

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))


@require_GET
@login_required
def resend_invite(request):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    if request.GET.get('id', ''):

        invite = Invitation.objects.get(id=request.GET.get('id'))
        invite.activation_key = 'EXPIRED'
        invite.save()

        activation_key = utils.generate_activation_key(invite.email)
        new_invite = Invitation(
            email=invite.email,
            invited_by=request.user,
            activation_key=activation_key
        )

        new_invite.save()

        utils.send_invitation(new_invite)
        messages.success(request, _('Your invitation has been resent!'))

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))


@require_GET
@login_required
def revoke_invite(request):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    if request.GET.get('id', ''):

        invite = Invitation.objects.get(id=request.GET.get('id'))
        invite.activation_key = 'REVOKED'
        invite.save()

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-users'}))


@login_required
def dashboard(request, page_type=''):

    u = request.user

    q = [Q(is_deleted=False)]
    exq = []
    filter_by_page = []

    columns = ['id', 'title', 'ticket_category', 'status', 'issue_type',
               'date_added', 'assigned_to__first_name']

    order_dash = ['-id']

    if page_type == 'my-assignments' and u.is_admin:
        q.append(Q(assigned_to=u))
        exq.append(Q(status='closed'))

    elif page_type == 'in-progress-tickets' and u.is_admin:
        q.append(Q(assigned_to=u) & Q(status="inprogress"))

    elif page_type == 'pending-tickets' and u.is_admin:
        q.append(Q(assigned_to=u) & Q(status="pending"))

    elif page_type == 'unassigned' and u.is_admin:
        q.append(Q(assigned_to__isnull=True))
        exq.append(Q(status='closed'))

    elif page_type == 'open-tickets' and u.is_admin:
        exq.append(Q(status='closed'))

    elif page_type == 'closed-tickets' and u.is_admin:
        q.append(Q(status='closed'))

    elif page_type == 'my-alerts':
        q.append(Q(ticket_alerts__user=u))

    elif page_type == 'my-tickets':
        q.append((Q(created_by=u) & Q(created_for=None)) | Q(created_for=u))

    elif page_type == 'my-named-tickets' and u.is_named:
        q.append(Q(company_association=u.company_association))

    elif page_type == 'named-open-tickets' and u.is_named:
        q.append(Q(company_association=u.company_association))
        exq.append(Q(status='closed'))

    elif page_type == 'named-closed-tickets' and u.is_named:
        q.append(Q(company_association=u.company_association) & Q(status='closed'))

    elif page_type == 'my-open-tickets':
        q.append((Q(created_by=u) & Q(created_for=None)) | Q(created_for=u))
        exq.append(Q(status='closed'))

    elif page_type == 'my-closed-tickets':
        q.append(
            ((Q(created_by=u) & Q(created_for=None)) | Q(created_for=u)) & Q(status='closed')
        )

    elif page_type == 'partner-tickets':
        client = request.GET.get('partner', None)
        if client:
            q.append(Q(company_association__name=client))

    elif page_type == 'company-users':
        return add_company_user(request)

    elif page_type == 'company-partners':
        return add_company_partner(request)

    elif page_type == 'company-booking':
        return book_meeting(request)

    elif page_type == 'my-profile':
        return my_profile(request)

    elif page_type == 'oxd-config':
        return oxd_form(request)

    elif page_type == 'all-tickets' and u.is_admin:
        pass

    elif page_type == 'view-users' and u.is_admin:
        return view_users(request, page_type)

    else:
        messages.error(request, _('You are not authorized to see requested page!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'})
        )

    filters = FilterTicketsForm(request.GET, user=request.user)

    if filters.is_valid():

        if filters.cleaned_data['named']:
            q.append(
                (Q(created_by__crm_type='named') & Q(created_for=None)) |
                Q(created_for__crm_type='named')
            )

        if filters.cleaned_data['status']:
            q.append(Q(status__in=filters.cleaned_data['status']))

        if filters.cleaned_data['category']:
            q.append(Q(ticket_category__in=filters.cleaned_data['category']))

        if filters.cleaned_data['issue_type']:
            if 'community' in filters.cleaned_data['issue_type']:
                q.append(
                    Q(issue_type__in=filters.cleaned_data['issue_type']) |
                    Q(issue_type='')
                )
            else:
                q.append(Q(issue_type__in=filters.cleaned_data['issue_type']))

        if filters.cleaned_data['company']:
            q.append(
                (Q(created_by__company__in=filters.cleaned_data['company']) & Q(created_for=None)) |
                Q(created_for__company__in=filters.cleaned_data['company'])
            )

        if filters.cleaned_data['assigned_to']:
            q.append(Q(assigned_to__in=filters.cleaned_data['assigned_to']))

        if filters.cleaned_data['created_by']:

            q.append(
                (Q(created_by__in=filters.cleaned_data['created_by']) & Q(created_for=None)) |
                Q(created_for__in=filters.cleaned_data['created_by'])
            )

        if filters.cleaned_data['created_date'] or filters.cleaned_data['created_filters']:

            dd = filters.cleaned_data['created_date']
            now = timezone.now()
            today = now.date()

            if filters.cleaned_data['created_filters'] == "eq" and dd:
                s, f = cstm_dates(dd, dd)
                q.append(Q(date_added__gte=s) & Q(date_added__lte=f))

            if filters.cleaned_data['created_filters'] == "not_eq" and dd:
                s, f = cstm_dates(dd, dd)
                q.append(Q(date_added__lt=s) & Q(date_added__gt=f))

            if filters.cleaned_data['created_filters'] == "gt" and dd:
                q.append(Q(date_added__gt=dd))

            if filters.cleaned_data['created_filters'] == "lt" and dd:
                q.append(Q(date_added__lt=dd))

            if filters.cleaned_data['created_filters'] == "last_7_days":
                last_7_days = now.date() - timedelta(days=7)
                s, f = cstm_dates(last_7_days, today)
                q.append(Q(date_added__gte=s) & Q(date_added__lte=f))

            if filters.cleaned_data['created_filters'] == "last_30_days":
                last_30_days = now.date() - timedelta(days=30)
                s, f = cstm_dates(last_30_days, today)
                q.append(Q(date_added__gte=s) & Q(date_added__lte=f))

            if filters.cleaned_data['created_filters'] == "last_month":
                first_last_month = today.replace(month=today.month - 1, day=1)
                last_last_month = today.replace(month=today.month, day=1)
                s, f = cstm_dates(first_last_month, last_last_month)
                q.append(Q(date_added__gte=s) & Q(date_added__lt=f))

            if filters.cleaned_data['created_filters'] == "this_month":
                this_month = today.replace(day=1)
                next_month = today.replace(month=today.month + 1, day=1)
                s, f = cstm_dates(this_month, next_month)
                q.append(Q(date_added__gte=s) & Q(date_added__lte=f))

            if filters.cleaned_data['created_filters'] == "last_year":
                last_year = today.replace(year=today.year - 1, month=1, day=1)
                q.append(Q(date_added__year=last_year.year))

            if filters.cleaned_data['created_filters'] == "this_year":
                q.append(Q(date_added__year=today.year))

    filter_by_page = q

    # TODO Decouple from the rest
    if request.method == 'POST':
        user_filters = []

        if 'search[value]' in request.POST and len(request.POST['search[value]']) >= 3:
            search_value = request.POST['search[value]'].strip()

            if len(search_value) == 3 and len(search_value.split(' ')) > 1:
                for word in search_value.split(' '):
                    user_filters.extend([
                        (Q(created_by__first_name=word) & Q(created_for=None)) |
                        Q(created_for__first_name=word) |
                        (Q(created_by__last_name=word) & Q(created_for=None)) |
                        Q(created_for__last_name=word) |
                        Q(assigned_to__first_name=word)
                    ])
            else:
                q.extend([
                    Q(id__icontains=request.POST['search[value]']) |
                    (Q(created_by__first_name=request.POST['search[value]']) & Q(created_for=None)) |
                    Q(created_for__first_name=request.POST['search[value]']) |
                    (Q(created_by__last_name=request.POST['search[value]']) & Q(created_for=None)) |
                    Q(created_for__last_name=request.POST['search[value]']) |
                    (Q(created_by__email__icontains=search_value) & Q(created_for=None)) |
                    Q(created_for__email__icontains=search_value) |
                    Q(ticket_category=request.POST['search[value]']) |
                    Q(status__icontains=request.POST['search[value]']) |
                    Q(issue_type__icontains=request.POST['search[value]']) |
                    Q(title__icontains=request.POST['search[value]']) |
                    Q(assigned_to__first_name__icontains=request.POST['search[value]'])
                    # Q(["CONCAT_WS(' ', profiles_userprofile.first_name, profiles_userprofile.last_name) like '"+request.POST['search[value]']+"' "])
                ])

        if 'order[0][column]' in request.POST:
            order_sign = '-' if request.POST['order[0][dir]'] == 'desc' else ''
            order_dash = ['%s%s' % (order_sign, columns[int(request.POST['order[0][column]'])])]

        results = {
            "draw": request.POST['draw'],
            "recordsTotal": 0,
            "recordsFiltered": int(request.POST['length']),
            "data":[]
        }
        cur = int(request.POST['start'])
        cur_length = int(request.POST['length']) + cur

        if len(user_filters) > 1:
            tickets = Ticket.objects.get_active(u).filter(*q).exclude(*exq).filter(*user_filters).order_by(*order_dash)[cur:cur_length]
        else:
            tickets = Ticket.objects.get_active(u).filter(*q).exclude(*exq).order_by(*order_dash)[cur:cur_length]

        if len(user_filters) > 1:
            results['recordsTotal'] = Ticket.objects.get_active(u).filter(*filter_by_page).exclude(*exq).filter(*user_filters).count()
            results['recordsFiltered'] = Ticket.objects.get_active(u).filter(*q).exclude(*exq).filter(*user_filters).count()
        else:
            results['recordsTotal'] = Ticket.objects.get_active(u).filter(*filter_by_page).exclude(*exq).count()
            results['recordsFiltered'] = Ticket.objects.get_active(u).filter(*q).exclude(*exq).count()
        staff = UserProfile.objects.filter(is_active=True, crm_type__in=['staff', 'admin', 'manager'])

        for t in tickets:
            support_level = ""
            support_plan = crm_interface.get_support_plan(t.owned_by)
            if support_plan:
                support_level = support_plan.get('support_plan')
                if support_level == "blank":
                    support_level = "Community"
            else:
                if t.owned_by.get_company() == "Gluu":
                    support_level="Staff"
                else:
                    support_level = "Community"
            ht = ''
            description = u'''
                <a style="display:block;font-size:15px;word-break: break-all;" href="{0}">{1}</a> by {2}
                <span data-toggle="tooltip" class="glyphicon glyphicon-info-sign" title="Company: {3} <br />
                    Support Level: {4} <br />
                    Last update by: {5} <br />
                    Last update: {6} <br />
                    Total responses: {7}">
                </span>'''.format(
                generate_ticket_link(t), t.title, t.owned_by, t.owned_by.get_company(), support_level, t.last_updated,
                get_fancy_time(t.date_modified), t.answers_no)

            if u.is_admin:
                ht = u'''<select data-ticket={0} class="dashboard_assign_staff" style="width:100px;" name="assigned_to">
                    <option selected value="">Assign ticket</option>'''.format(t.id)
                for u in staff:
                    selected = ''
                    if t.assigned_to == u:
                        selected = 'selected'
                    ht += u'''<option {0} value="{1}">{2}</option>'''.format(selected, u.id, u)
                ht += '</select>'

            row = [t.id,
                   description,
                   t.get_ticket_category_display(),
                   '<span class="label-table label-{0}">{1}</span>'.format(t.status.lower(), t.status),
                   '<span class="label-table label-{0}">{1}</span>'.format(t.priority, t.priority),
                   '{:%m-%d-%Y}'.format(t.date_added)]
            if ht != '':
                row.append(ht)

            results["data"].append(row)

        return HttpResponse(json.dumps(results), content_type="application/json")

    clients = Company.objects.filter(
        clients__is_deleted=False,
        clients__partner=request.user.company_association
    )
    support_details = {}
    try:
        support_details = utils.get_support_details(request)
    except (KeyError, TypeError) as e:

        log_crm('Unexpected support plan value: {}, {}'.format(support_details, e), 'ERROR')
        pass

    return render(
        request,
        'profiles/dashboard.html', {
            'page': 'dashboard',
            'filters_form': filters,
            'page_type': page_type,
            'clients': clients,
            'support_details': support_details
        }
    )


@login_required
def my_profile(request):

    if request.method == 'POST':

        try:
            profile_form = ProfileForm(
                request.POST,
                instance=request.user
            )

            if profile_form.is_valid():

                profile_form.save()

                if profile_form.changed_data:
                    idp_interface.update_user(request.user)
                    # crm_interface.update_contact(request.user)

                messages.success(request, _('Profile has been successfully changed'))

            else:

                messages.error(request, _('Changes could not be made. Please check form for errors.'))

        except Exception as e:

            logger.exception(e)
            return HttpResponseServerError()

    else:

        profile_form = ProfileForm(instance=request.user)

    support_details={}
    try:
        support_details = utils.get_support_details(request)
    except (KeyError, TypeError) as e:

        log_crm('Unexpected support plan value: {}, {}'.format(support_details, e), 'ERROR')
        pass

    return render(request, 'profiles/edit_profile.html', {
        'profile_form': profile_form,
        'page_type': 'my-profile',
        'support_details': support_details
    })

@login_required
def oxd_form(request):

    if request.method == 'POST':

        oxd_form= OxdConfigurationForm
        config = configparser.ConfigParser()
        this_dir = os.path.dirname(os.path.realpath(__file__))
        config_location = os.path.join(this_dir, 'gluu.cfg')
        config.read(config_location)
        oxd_host = config.set('oxd', 'host' , request.POST.get('oxd_host'))
        oxd_port = config.set('oxd','port',request.POST.get('oxd_port'))
        oxd_id = config.set('oxd','id','')
        client_op_host = config.set('client','op_host',request.POST.get('client_op_host'))
        client_authorization_redirect_uri = config.set('client','authorization_redirect_uri',request.POST.get('client_authorization_redirect_uri'))
        client_post_logout_redirect_uri = config.set('client','post_logout_redirect_uri',request.POST.get('client_post_logout_redirect_uri'))
        client_scope = config.set('client','scope',request.POST.get('client_scope'))
        client_id = config.set('client','client_id',request.POST.get('client_id'))
        client_secret = config.set('client','client_secret',request.POST.get('client_secret'))
        client_grant_types = config.set('client','grant_types',request.POST.get('client_grant_types'))
        client_id_issued_at = config.set('client','client_id_issued_at',request.POST.get('client_id_issued_at'))

        with open(config_location, 'w') as configfile:
            config.write(configfile)
        response= setup_client(request, render_page=False)
        if response["status"] == "ok":
            messages.success(request, _(response["message"]))
        else:
            messages.warning(request,_(response["message"]))
    else:
        oxd_form= OxdConfigurationForm

    return render(request, 'profiles/oxd_form.html', {
        'oxdConfigurationForm': oxd_form,
        'page_type': 'oxd-config',
    })

@login_required
def view_users(request, page_type):
    if request.method == "POST":
        user = UserProfile.objects.filter(id=request.POST['user_id']).values()
        results = {
            "data": list(user)
        }
        return JsonResponse(results, status=200)
    else:
        users = UserProfile.objects.filter(is_active=True)
        return render(request, 'profiles/view_users.html', {
            'users': users,
            'page_type': page_type
        })


@login_required
def ticket_activation(request):
    if request.method == "POST" and request.POST['action'] == "activate_ticket":
        ticket_id = request.POST['ticket_id']
        Ticket.objects.filter(id=ticket_id).update(is_deleted=0)
        Answer.objects.filter(ticket_id=ticket_id).update(is_deleted=0)
        results = {"success": 1}
        return JsonResponse(results, status=200)
    else:
        results = {"success": 0}
        return JsonResponse(results, status=400)


@require_GET
def inactive_user(request):

    return render(request, 'error.html', {
        'error': 'Inactive User',
        'description': 'The user account you tried to log in with has been disabled.'
    })


@login_required
def add_company_partner(request):

    if request.user.crm_type != 'named':

        return HttpResponseRedirect(reverse('home'))

    client = request.user.company_association

    if request.method == 'POST':

        partner_form = PartnerForm(request.POST)

        if partner_form.is_valid():

            partner = Company.objects.get(
                name=partner_form.cleaned_data.get('partner'))

            if client == partner:

                messages.error(request, _(
                    'Partner company must be different from your own company.'))

            else:

                try:

                    Partnership.objects.get(partner=partner, client=client, is_deleted=False)

                except ObjectDoesNotExist:

                    partnership = Partnership(partner=partner, client=client)
                    partnership.save()

                    utils.send_new_partner_notification(
                        partner=partner,
                        client=client,
                        company_admin=request.user
                    )

                    # crm_interface.add_partnership(partnership)

                    messages.success(request, _('Partner has been added.'))

                return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-partners'}))
    else:

        partner_form = PartnerForm()

    partnerships = Partnership.objects.filter(client=client, is_deleted=False)

    support_details={}
    try:
        support_details = utils.get_support_details(request)
    except (KeyError, TypeError) as e:

        log_crm('Unexpected support plan value: {}, {}'.format(support_details, e), 'ERROR')
        pass

    return render(request, 'profiles/my_partners.html', {
        'page_type': 'company-partners',
        'partnerships': partnerships,
        'partner_form': partner_form,
        'support_details': support_details
    })


@require_GET
@login_required
def revoke_partner(request, partnership_id):

    if request.user.crm_type != 'named' or not request.user.is_company_admin:

        return HttpResponseRedirect(reverse('home'))

    try:
        partnership = Partnership.objects.get(id=partnership_id)

        if request.user.company_association == partnership.client:

            partnership.is_deleted = True
            partnership.save()

            utils.send_partnership_revoked_notification(
                partner=partnership.partner,
                client=partnership.client,
                company_admin=request.user
            )

            # crm_interface.remove_partnership(partnership)

            messages.success(request, _('Company has been removed from Partners.'))

        else:
            log_error('Error Revoking Partnership Access: Partnership {}, User {}'.format(
                partnership.id, request.user.email))

    except ObjectDoesNotExist:

        log_error('Error Revoking Access of Named Account: User not found')

    return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'page_type': 'company-partners'}))


@login_required
def book_meeting(request):

    if request.user.crm_type != 'named':

        return HttpResponseRedirect(reverse('home'))

    support_details = {}

    try:

       support_details = utils.get_support_details(request)

    except (KeyError, TypeError) as e:

        log_crm('Unexpected support plan value: {}, {}'.format(support_details, e), 'ERROR')
        pass

    return render(request, 'profiles/book_meeting.html', {
        'page_type': 'company-booking',
        'support_details': support_details
    })


@login_required
def accept_invite(request, activation_key):

    try:

        invitation = Invitation.objects.get(activation_key=activation_key)

        if request.user.email != invitation.email:

            return render(request, 'error.html', {
                'error': 'Email Mismatch',
                'description': 'The invitation was not meant for to that email.'
            })

        user = request.user

        user.crm_type = 'named'
        user.company_association = invitation.invited_by.company_association
        user.company = invitation.invited_by.company_association.name
        user.save()

        invitation.activation_key = 'ACTIVATED'
        invitation.save()

        # crm_interface.upgrade_user_record(user)
        utils.send_new_user_notification(user)

        return HttpResponseRedirect(reverse('home'))

    except Exception as e:

        logger.exception(e)

        return render(request, 'error.html', {
            'error': 'Invitation Key not recognized',
            'description': 'Sorry, we did not recognize that invitation key. \
                            It either has been used before or is invalid.',
        })
