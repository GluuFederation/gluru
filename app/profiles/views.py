import logging
import urllib
import urllib2
import json
import re
import os
import configparser
import xlwt
import csv
import oxdpython
from datetime import timedelta
from profiles.gluu_oxd import setup_client
from django.conf import settings
from main import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponsePermanentRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from social.apps.django_app.default.models import UserSocialAuth

from main.utils import cstm_dates, get_fancy_time, log_error, log_crm, format_minutes

from profiles import constants
from profiles.forms import (
    ProfileForm, RegistrationForm, InvitationForm, NamedRegistrationForm, PartnerForm, OxdConfigurationForm)
from profiles.models import UserProfile, Activation, Invitation, Company, Partnership, OxdConfiguration, Registration
from profiles import utils, tasks

from tickets.models import Ticket, Answer
from tickets.forms import FilterTicketsForm
from tickets.utils import generate_ticket_link

from connectors.sugarcrm import crm_interface
from connectors.idp import idp_interface
import base64

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


def register(request, name=''):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST,request=request)
        try:
            if request.POST.get('email', None):
                if registration_form.is_valid():
                    recaptcha_response = request.POST.get('g-recaptcha-response')
                    url = 'https://www.google.com/recaptcha/api/siteverify'
                    values = {
                        'secret': settings.RECAPTCHA_PRIVATE_KEY,
                        'response': recaptcha_response
                    }
                    data = urllib.urlencode(values)
                    req = urllib2.Request(url, data)
                    response = urllib2.urlopen(req)
                    result = json.load(response)
                    if result['success']:
                        user = registration_form.save(commit=False)
                        user.is_active = False
                        user.save()
                        tasks.send_activation_email.apply_async(args=[user.id], expires=60)
                    # registration = Registration(status = 'initial', user_id=user.id)
                    # registration.save()
                    	return render(request, 'profiles/registration_complete.html', {'email': user.email})
                    else:
                        messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            else:
                if registration_form.is_valid():
                    split_request = request.path.split('/')[:-1]
                    split_url = split_request[2]
                    decode_email = '{0}'.format(split_url)
                    decode_email = decode_email.replace("_", "=")
                    url_splited = base64.urlsafe_b64decode(decode_email)
                    final_url = url_splited.split('$')
                    email = final_url[0]
                    activation_key = final_url[1]

                    activation = Activation.objects.get(activation_key=activation_key)
                    activation.activation_key = 'ACTIVATED'
                    activation.save()

                    user = UserProfile.objects.get(email=email)
                    crm_interface.sync_basic_user_with_crm(user)
                    user.is_active = True
                    user.company = request.POST.get('company')
                    user.password = request.POST['password1']
                    user.job_title = request.POST['job_title']
                    user.mobile_number = request.POST['mobile_number']
                    user.timezone = request.POST['timezone']
                    user.save()
                    #Registration.objects.filter(user_id=user.id).update(status='pending', idp_password=user.password)
                    #registration = Registration(status='pending', user_id=user.id)
                    #registration.save()
                    tasks.confirm_registration.apply_async(args=[user.id, registration_form.cleaned_data.get('password1')], expires=60)
                    messages.success(request, _('Thank you for registering on Gluu Support! You can now sign in.'))
                    return HttpResponseRedirect(reverse('home'))
        except Exception as e:
            logger.exception(e)
            return render(request, 'error.html', {
                'error': 'Registration Failed',
                'description': 'Something went wrong.',
            })

    else:
            registration_form = RegistrationForm(request=request)
    return render(request, 'profiles/register.html', {
        'page_type': 'registered',
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
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                     'secret': settings.RECAPTCHA_PRIVATE_KEY,
                     'response': recaptcha_response
                }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                result = json.load(response)
                if result['success']:
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
                    crm_interface.upgrade_user_record(user)
                    utils.send_new_user_notification(user)
                    utils.send_activate_account_notification(user)
                    messages.success(request, _('Your account has been activated! You can login.'))
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

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
            user = activation.user
            company = user.email.split("@")[1]
            email_suffixes = {company: user.email}
            if company in email_suffixes.keys() and company not in ['aol.com', 'fastmail.fm', 'fastmailbox.net', 'gmail.com', 'gmx.at', 'gmx.de', 'gmx.li', 'gmx.net', 'hushmail.com', 'icloud.com',
                                                                    'lycos.co.uk','lycos.com',
             'lycos.es','lycos.it','lycos.ne.jp','lycosemail.com','lycosmail.com','email.com','email.cz','email.ee',
             'email.it','email.nu','email.ro','email.ru','email.si','outlook.com','hotmail.com','runbox.com',
             'yahoo.ca','yahoo.co.in','yahoo.co.jp','yahoo.co.kr','yahoo.co.nz','yahoo.co.uk','yahoo.com',
             'yahoo.com.ar','yahoo.com.au','yahoo.com.br','yahoo.com.cn','yahoo.com.hk','yahoo.com.is','yahoo.com.mx',
             'yahoo.com.ru','yahoo.com.sg','yahoo.de','yahoo.dk','yahoo.es','yahoo.fr','yahoo.ie','yahoo.it',
             'yahoo.jp','yahoo.ru','yahoo.se','yahoofs.com','yandex.ru','zoho.com','yendex.com','tutanota.com', 'ymail.com']:
                try:
                    query = ''' SELECT profiles_userprofile.company
                            FROM profiles_userprofile
                            INNER JOIN profiles_company ON profiles_userprofile.company_association_id = profiles_company.id
                            WHERE profiles_userprofile.email like '%{0}%';
                           '''.format(company)
                    cursor = connection.cursor()
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            user_company = row[0]
                    else:
                        query = "SELECT `company` FROM `profiles_userprofile` WHERE `email` LIKE '%{0}%'  LIMIT 0,1;".format(company)
                        cursor = connection.cursor()
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        if rows:
                            for row in rows:
                                user_company = row[0]
                        else:
                            user_company = "N/A"


                except Exception as e:
                    logger.exception(e)
            else:
                user_company = "N/A"

            encoded_email = base64.urlsafe_b64encode("{0}${1}${2}".format(user.email, activation_key, user_company))
            encoded_email = encoded_email.replace("=", "_")
            messages.success(request, _('Welcome to the Gluu Support Portal.'))
            return HttpResponsePermanentRedirect(reverse('profile:registered', kwargs={'name':encoded_email }))

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
                    account.company = request.user.company
                    account.company_association = request.user.company_association
                    account.crm_type = request.user.crm_type
                    account.is_staff = request.user.is_staff
                    account.save()

                    crm_interface.upgrade_user_record(account)

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

            crm_interface.update_account_admin_status(user)

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

        crm_interface.update_account_admin_status(user, downgrade=True)

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

    elif page_type == 'export_users' and u.is_admin:
       return export_users(request)

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
                    idp_interface.update_user(request.user, password=False)
                    crm_interface.update_contact(request.user)

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

        try:
            oxd_configuration = OxdConfiguration.objects.get(Q(oxd_host=request.POST.get('oxd_host')) & Q(client_op_host=request.POST.get('client_op_host')) & Q(client_authorization_redirect_uri=request.POST.get('client_authorization_redirect_uri')))
            if oxd_configuration:
                if request.POST.get('oxd_https_extension') == "true" and oxd_configuration.is_https_extension:
                    config.set('oxd', 'host', request.POST.get('oxd_host')+':'+request.POST.get('oxd_port'))
                    config.remove_option('oxd', 'port')
                    config.set('oxd', 'https_extension', 'True')
                    config.set('oxd', 'id', oxd_configuration.oxd_id)
                    config.set('client', 'client_name', request.POST.get('client_name'))
                    config.set('client', 'client_id', oxd_configuration.client_id)
                    config.set('client', 'client_secret', oxd_configuration.client_secret)
                    config.set('client', 'op_host', oxd_configuration.client_op_host)
                    config.set('client', 'authorization_redirect_uri', oxd_configuration.client_authorization_redirect_uri)
                    config.set('client', 'client_id_issued_at', oxd_configuration.created_at)
                    config.set('client', 'post_logout_redirect_uri', request.POST.get('client_post_logout_redirect_uri'))
                    config.set('client', 'scope', request.POST.get('client_scope'))
                    config.set('client', 'grant_types', request.POST.get('client_grant_types'))
                    config.set('client', 'client_id_issued_at', oxd_configuration.created_at)
                elif request.POST.get('oxd_https_extension') == "false" and not oxd_configuration.is_https_extension:
                    config.set('oxd', 'host', request.POST.get('oxd_host'))
                    config.set('oxd', 'port', request.POST.get('oxd_port'))
                    config.remove_option('oxd','https_extension')
                    config.set('oxd', 'id', oxd_configuration.oxd_id)
                    config.set('client', 'client_name', request.POST.get('client_name'))
                    config.set('client', 'client_id', oxd_configuration.client_id)
                    config.set('client', 'client_secret', oxd_configuration.client_secret)
                    config.set('client', 'op_host', oxd_configuration.client_op_host)
                    config.set('client', 'authorization_redirect_uri', oxd_configuration.client_authorization_redirect_uri)
                    config.set('client', 'client_id_issued_at', oxd_configuration.created_at)
                    config.set('client', 'post_logout_redirect_uri', request.POST.get('client_post_logout_redirect_uri'))
                    config.set('client', 'scope', request.POST.get('client_scope'))
                    config.set('client', 'grant_types', request.POST.get('client_grant_types'))
                    config.set('client', 'client_id_issued_at', oxd_configuration.created_at)
                messages.success(request,"Client Setup successful!!")
                try:
                    OxdConfiguration.objects.filter(is_active=True).update(is_active=False)
                except:
                    pass
                OxdConfiguration.objects.filter(Q(oxd_host=request.POST.get('oxd_host')) & Q(client_op_host=request.POST.get('client_op_host')) & Q(client_authorization_redirect_uri=request.POST.get('client_authorization_redirect_uri'))).update(is_active=True)

        except:
            if request.POST.get('oxd_https_extension') == "true":
                config.set('oxd', 'host', request.POST.get('oxd_host')+':'+request.POST.get('oxd_port'))
                config.set('client', 'client_name', request.POST.get('client_name'))
                config.set('client','op_host',request.POST.get('client_op_host'))
                config.set('client','authorization_redirect_uri',request.POST.get('client_authorization_redirect_uri'))
                config.set('client','post_logout_redirect_uri',request.POST.get('client_post_logout_redirect_uri'))
                config.set('client', 'scope', "openid,profile,email")
                config.set('client', 'grant_types', "authorization_code,client_credentials")
                config.set('client', 'client_id_issued_at', request.POST.get('client_id_issued_at'))
                config.set('oxd', 'id', '')
                config.set('client', 'client_id', '')
                config.set('client', 'client_secret', '')
                try:
                    config.get('oxd', 'https_extension')
                except:
                    config.set('oxd', 'https_extension', 'True')
                with open(config_location, 'w') as configfile:
                    config.write(configfile)
                response = setup_client(request, render_page=False)
                if response["status"] == "ok":
                    config.set('oxd','id',response['setup_client_oxd_id'])
                    config.set('client','client_id',response['client_id'])
                    config.set('client','client_secret',response['client_secret'])
                    config.set('client','op_host',request.POST.get('client_op_host'))
                    config.set('client', 'authorization_redirect_uri', request.POST.get('client_authorization_redirect_uri'))
                    config.set('client', 'client_secret_expires_at', '1560402491000')
                    with open(config_location, 'w') as configfile:
                         config.write(configfile)
                    client = oxdpython.Client(config_location)
                    client.get_client_token()
                    client.update_site(client_secret_expires_at='1560402491000')
                    config.set('oxd','id',response['oxd_id'])
                    with open(config_location, 'w') as configfile:
                         config.write(configfile)
                    client = oxdpython.Client(config_location)
                    client.get_client_token()
                    client.update_site(client_secret_expires_at='1560402491000')
                    try:
                        OxdConfiguration.objects.filter(is_active=True).update(is_active=False)
                    except:
                        pass
                    OxdConfiguration.objects.create(oxd_host=request.POST.get('oxd_host'),oxd_port=request.POST.get('oxd_port'),oxd_id=response['oxd_id'],client_op_host=request.POST.get('client_op_host'),
                                           client_authorization_redirect_uri=request.POST.get('client_authorization_redirect_uri'),client_id=response['client_id'],client_secret=response['client_secret'],
                                           is_https_extension=True, is_active=True)
                    messages.success(request, _(response["message"]))
                else:
                    try:
                        result = OxdConfiguration.objects.get(is_active=True)
                        if result.is_https_extension:
                            config.set('oxd', 'host', str(result.oxd_host)+':'+str(result.oxd_port))
                            config.remove_option('oxd', 'port')
                            config.set('oxd','https_extension','True')
                        else:
                            config.set('oxd', 'host', result.oxd_host)
                            config.set('oxd', 'port', result.oxd_port)
                            config.remove_option('oxd','https_extension')
                        config.set('oxd','id',result.oxd_id)
                        config.set('client','client_id',result.client_id)
                        config.set('client','client_secret',result.client_secret)
                        config.set('client', 'authorization_redirect_uri', result.client_authorization_redirect_uri)
                        config.set('client', 'client_id_issued_at', result.created_at)
                        messages.error(request, response['message'])
                    except:
                        messages.error(request, response['message'])

            elif request.POST.get('oxd_https_extension') == "false":
                config.set('oxd', 'host', request.POST.get('oxd_host'))
                config.set('oxd', 'port', request.POST.get('oxd_port'))
                config.set('client', 'client_name', request.POST.get('client_name'))
                config.set('client','op_host',request.POST.get('client_op_host'))
                config.set('client','authorization_redirect_uri',request.POST.get('client_authorization_redirect_uri'))
                config.set('client','post_logout_redirect_uri',request.POST.get('client_post_logout_redirect_uri'))
                config.set('client', 'scope', "openid,profile,email")
                config.set('client', 'grant_types', "authorization_code,client_credentials")
                config.set('client', 'client_id_issued_at', request.POST.get('client_id_issued_at'))
                config.set('oxd', 'id', '')
                config.set('client', 'client_id', '')
                config.set('client', 'client_secret', '')
                try:
                    config.get('oxd', 'https_extension')
                    config.remove_option('oxd', 'https_extension')
                except:
                    pass
                with open(config_location, 'w') as configfile:
                    config.write(configfile)
                response = setup_client(request, render_page=False)
                if response["status"] == "ok":
                    config.set('oxd','id',response['setup_client_oxd_id'])
                    config.set('client','client_id',response['client_id'])
                    config.set('client','client_secret',response['client_secret'])
                    config.set('client','op_host',request.POST.get('client_op_host'))
                    config.set('client', 'authorization_redirect_uri', request.POST.get('client_authorization_redirect_uri'))
                    config.set('client', 'client_secret_expires_at', '1560402491000')
                    with open(config_location, 'w') as configfile:
                         config.write(configfile)
                    client = oxdpython.Client(config_location)
                    client.get_client_token()
                    client.update_site(client_secret_expires_at='1560402491000')
                    config.set('oxd','id',response['oxd_id'])
                    with open(config_location, 'w') as configfile:
                         config.write(configfile)
                    client = oxdpython.Client(config_location)
                    client.get_client_token()
                    client.update_site(client_secret_expires_at='1560402491000')
                    try:
                        OxdConfiguration.objects.filter(is_active=True).update(is_active=False)
                    except:
                        pass
                    OxdConfiguration.objects.create(oxd_host=request.POST.get('oxd_host'),oxd_port=request.POST.get('oxd_port'),oxd_id=response['oxd_id'],client_op_host=request.POST.get('client_op_host'),
                                           client_authorization_redirect_uri=request.POST.get('client_authorization_redirect_uri'),client_id=response['client_id'],client_secret=response['client_secret'],
                                           is_https_extension=False, is_active=True)
                    messages.success(request, _(response["message"]))
                else:
                    try:
                        result = OxdConfiguration.objects.get(is_active=True)
                        config.set('oxd', 'host', result.oxd_host)
                        config.set('oxd', 'port', result.oxd_port)
                        config.remove_option('oxd','https_extension')
                        config.set('oxd','id',result.oxd_id)
                        config.set('client','client_id',result.client_id)
                        config.set('client','client_secret',result.client_secret)
                        config.set('client', 'authorization_redirect_uri', result.client_authorization_redirect_uri)
                        config.set('client', 'client_id_issued_at', result.created_at)
                        messages.error(request,response['message'])
                    except:
                        messages.error(request,response['message'])


        with open(config_location, 'w') as configfile:
            config.write(configfile)
    else:
        oxd_form= OxdConfigurationForm

    return render(request, 'profiles/oxd_form.html', {
        'oxdConfigurationForm': oxd_form,
        'page_type': 'oxd-config',
    })

@login_required
def reset_oxd_values(request):
    config = configparser.ConfigParser()
    this_dir = os.path.dirname(os.path.realpath(__file__))
    config_location = os.path.join(this_dir, 'gluu.cfg')
    config.read(config_location)
    config.set('oxd', 'host', '')
    config.set('oxd', 'port', '')
    config.remove_option('oxd', 'https_extension')
    config.set('oxd', 'id', '')
    config.set('client', 'client_name', '')
    config.set('client', 'client_id', '')
    config.set('client', 'client_secret', '')
    config.set('client', 'op_host', '')
    config.set('client', 'authorization_redirect_uri', '')
    config.set('client', 'post_logout_redirect_uri', '')
    config.set('client', 'scope', '')
    config.set('client', 'grant_types', '')
    config.set('client', 'client_id_issued_at', '')
    config.set('client', 'client_secret_expires_at', '')
    with open(config_location, 'w') as configfile:
            config.write(configfile)
    try:
        oxd_configuration = OxdConfiguration.objects.get(is_active=True).delete()
    except:
        pass
    return HttpResponse(json.dumps({'success': 'true'}),
                  content_type='application/json')

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
       plan = [ 'Community','Basic', 'Standard', 'Premium', 'Enterprise', 'Partner']
       return render(request, 'profiles/view_users.html', {
           'users': users,
           'page_type': page_type,
           'plan': plan
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

                    crm_interface.add_partnership(partnership)

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

            crm_interface.remove_partnership(partnership)

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

        crm_interface.upgrade_user_record(user)
        utils.send_new_user_notification(user)

        return HttpResponseRedirect(reverse('home'))

    except Exception as e:

        logger.exception(e)

        return render(request, 'error.html', {
            'error': 'Invitation Key not recognized',
            'description': 'Sorry, we did not recognize that invitation key. \
                            It either has been used before or is invalid.',
        })


@login_required
def export_users(request):
   if request.user.is_admin:
       response = HttpResponse(content_type='text/csv')
       response['Content-Disposition'] = 'attachment; filename=users.csv'
       writer = csv.writer(response, csv.excel)
       response.write(u'\ufeff'.encode('utf8'))
       writer.writerow([
           smart_str(u"Username"),
           smart_str(u"First name"),
           smart_str(u"Last name"),
           smart_str(u"Email address"),
           smart_str(u"Mobile Number"),
           smart_str(u"Company"),
           smart_str(u"Support Plan"),
           smart_str(u"Type")
       ])
       cursor = connection.cursor()
       get_request = request.GET
       try:
           if get_request.get('all_users', None) == "custom_users":
               if get_request.get('plan_users', None) == "Community":
                   query = '''
                              SELECT
                                   profiles_userprofile.username,
                                   profiles_userprofile.first_name,
                                   profiles_userprofile.last_name,
                                   profiles_userprofile.email,
                                   profiles_userprofile.mobile_number,
                                   profiles_userprofile.company,
                                   profiles_company.support_plan
                              FROM  profiles_userprofile
                              INNER JOIN
                                    profiles_company
                              WHERE {0}
                       '''.format(get_data(get_request))
               else:
                   query = '''
                              SELECT
                                    profiles_userprofile.username,
                                    profiles_userprofile.first_name,
                                    profiles_userprofile.last_name,
                                    profiles_userprofile.email,
                                    profiles_userprofile.mobile_number,
                                    profiles_userprofile.company,
                                    profiles_company.support_plan,
                                    profiles_company.type
                                FROM
                                    profiles_userprofile
                                        INNER JOIN
                                    profiles_company ON profiles_userprofile.company_association_id = profiles_company.id
                                WHERE {0}
                       '''.format(get_data(get_request))
           elif get_request.get('all_users', None) == "all_users":
               query = '''
                    SELECT
                          profiles_userprofile.username,
                          profiles_userprofile.first_name,
                          profiles_userprofile.last_name,
                          profiles_userprofile.email,
                          profiles_userprofile.mobile_number,
                          profiles_userprofile.company,
                          profiles_company.support_plan,
                          profiles_company.type
                      FROM
                          profiles_userprofile
                      LEFT JOIN
                          profiles_company ON profiles_userprofile.company_association_id = profiles_company.id
                      WHERE {0}
               '''.format(get_all_users_data(get_request))
           if get_request.get('users', None) == "All":
               response['Content-Disposition'] = 'attachment; filename= all-users.csv'
           else:
               response['Content-Disposition'] = 'attachment; filename= {0}-users.csv'.format(export_extention(get_request))
           cursor.execute(query)
           rows = cursor.fetchall()
           for row in rows:
               try:
                   writer.writerow(row)
               except Exception:
                   pass
           return response
       except Exception as e:
           logger.exception(e)
def get_data(get_request):
   list = get_request.getlist('plan_users', None)
   if get_request.get('all_users', None) == "custom_users":
       if get_request.get('plan_users', None) == "Community":
           if get_request.get('inactive_users', None) and get_request.get('active_users', None):
               data = '''
                   profiles_userprofile.is_active IN (1,0)
                   AND profiles_userprofile.company_association_id IS NULL
                   AND profiles_userprofile.crm_type IN ('user')
                   AND profiles_company.support_plan IN ('{0}');
                   '''.format("','".join(list))
           elif get_request.get('inactive_users', None):
               data = '''
                   profiles_userprofile.is_active = 0
                   AND profiles_userprofile.company_association_id IS NULL
                   AND profiles_userprofile.crm_type IN ('user')
                   AND profiles_company.support_plan IN ('{0}');
                   '''.format("','".join(list))
           else:
               data = '''
                   profiles_userprofile.is_active = 1
                   AND profiles_userprofile.company_association_id IS NULL
                   AND profiles_userprofile.crm_type IN ('user')
                   AND profiles_company.support_plan IN ('{0}');
                   '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
               'inactive_users', None) and get_request.get('active_users', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active IN (1,0)
               AND profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
               'inactive_users', None) and get_request.get('active_users', None) and get_request.get('inactive_users', None):
           data = '''
           profiles_userprofile.is_active IN (1,0)
           AND profiles_company.type IN ('Customer','ex_customer')
           AND profiles_userprofile.crm_type NOT IN ('staff')
           AND profiles_company.support_plan IN ('{0}');
           '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
               'active_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('active_users', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active = 0
               AND profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
               'inactive_users', None):
           data = '''
               profiles_userprofile.is_active = 0
               AND profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('ex_customer', None) and get_request.get( 'active_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_company.type IN ('ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('ex_customer', None) and get_request.get('active_users', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_company.type IN ('ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('active_users', None) and get_request.get(
               'inactive_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active IN (1,0)
               AND profiles_company.type IN ('Customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('active_users', None) and get_request.get(
               'inactive_users', None):
           data = '''
           profiles_userprofile.is_active IN (1,0)
           AND profiles_company.type IN ('Customer')
           AND profiles_userprofile.crm_type NOT IN ('staff')
           AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
           AND profiles_company.type NOT IN ('ex_customer')
           AND profiles_company.support_plan IN ('{0}');
           '''.format("','".join(list))
       elif get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
               'inactive_users', None) and get_request.get('managed_service', None):
           data = '''
           profiles_userprofile.is_active IN (1,0)
           AND profiles_company.type IN ('ex_ustomer')
           AND profiles_userprofile.crm_type NOT IN ('staff')
           AND profiles_company.support_plan IN ('{0}')
           AND profiles_company.managed_service = 1;
           '''.format("','".join(list))
       elif get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
               'inactive_users', None):
           data = '''
       profiles_userprofile.is_active IN (1,0)
       AND profiles_company.type IN ('ex_ustomer')
       AND profiles_userprofile.crm_type NOT IN ('staff')
       AND profiles_company.support_plan IN ('{0}');
       '''.format("','".join(list))
       elif get_request.get('active_users', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active IN (1, 0)
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('active_users', None) and get_request.get('inactive_users', None):
           data = '''
               profiles_userprofile.is_active IN (1, 0)
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('managed_service', None):
           data = '''
               profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('ex_customer', None):
           data = '''
               profiles_company.type IN ('Customer','ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif  get_request.get('active_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('active_users', None):
           data = '''
               profiles_userprofile.is_active = 1
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('inactive_users', None) and get_request.get('managed_service', None):
           data = '''
               profiles_userprofile.is_active = 0
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('inactive_users', None):
           data = '''
               profiles_userprofile.is_active = 0
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('customer', None) and get_request.get('managed_service', None):
           data = '''
               profiles_company.type IN ('Customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
       elif get_request.get('customer', None):
           data = '''
               profiles_company.type IN ('Customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}');
               '''.format("','".join(list))
       elif get_request.get('ex_customer', None) and get_request.get('managed_service', None):
           data = '''
               profiles_company.type IN ('ex_customer')
               AND profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan IN ('{0}')
               AND profiles_company.managed_service = 1;
               '''.format("','".join(list))
   else:
       data = '''
               profiles_userprofile.crm_type NOT IN ('staff')
               AND profiles_company.support_plan NOT IN ('ex_customer' , ' ')
               AND profiles_company.type NOT IN ('ex_customer')
               AND profiles_company.support_plan IN ('{0}');
        '''.format("','".join(list))
   return data

def get_all_users_data(get_request):
    if get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
            'inactive_users', None):
        query = '''
                 profiles_userprofile.is_active IN (1,0)
                 AND profiles_company.type IN ('ex_customer', 'Customer')
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
            'inactive_users', None) and get_request.get('managed_service', None):
        query = '''
             profiles_userprofile.is_active IN (1,0)
             AND profiles_company.type IN ('ex_customer', 'Customer')
             AND profiles_company.managed_service = 1
             '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('ex_customer', 'Customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('active_users',
                                                                                                        None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('ex_customer', 'Customer')
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
            'inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_company.type IN ('ex_customer','Customer')
                 AND profiles_userprofile.is_active = 0
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get(
            'inactive_users', None):
        query = '''
             profiles_company.type IN ('ex_customer','Customer')
             AND profiles_userprofile.is_active = 0
             '''
    elif get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
            'inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active IN (1, 0)
                 AND profiles_company.type IN ('ex_customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get(
            'inactive_users', None):
        query = '''
             profiles_userprofile.is_active IN (1, 0)
             AND profiles_company.type IN ('ex_customer')
             '''
    elif get_request.get('customer', None) and get_request.get('active_users', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active IN (1,0)
                 AND profiles_company.type IN ('Customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('active_users', None) and get_request.get(
            'inactive_users', None):
        query = '''
                 profiles_userprofile.is_active IN (1,0)
                 AND profiles_company.type IN ('Customer')
                 '''
    elif get_request.get('active_users', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active IN (1, 0)
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('active_users', None) and get_request.get('inactive_users', None):
        query = '''
                 profiles_userprofile.is_active IN (1, 0)
                 '''
    elif get_request.get('customer', None) and get_request.get('active_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('Customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('active_users', None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('Customer')
                 '''
    elif get_request.get('customer', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active = 0
                 AND profiles_company.type IN ('Customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('inactive_users', None):
        query = '''
                 profiles_userprofile.is_active = 0
                 AND profiles_company.type IN ('Customer')
                 '''
    elif get_request.get('ex_customer', None) and get_request.get('active_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('ex_customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('ex_customer', None) and get_request.get('active_users', None):
        query = '''
                 profiles_userprofile.is_active = 1
                 AND profiles_company.type IN ('ex_customer')
                 '''
    elif get_request.get('ex_customer', None) and get_request.get('inactive_users', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_userprofile.is_active = 0
                 AND profiles_company.type IN ('ex_customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('ex_customer', None) and get_request.get('inactive_users', None):
        query = '''
                 profiles_userprofile.is_active = 0
                 AND profiles_company.type IN ('ex_customer')
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None) and get_request.get('managed_service', None):
        query = '''
                 profiles_company.type IN ('ex_customer', 'Customer')
                 AND profiles_company.managed_service = 1
                 '''
    elif get_request.get('customer', None) and get_request.get('ex_customer', None):
        query = '''
                 profiles_company.type IN ('ex_customer', 'Customer')
                 '''
    elif get_request.get('active_users', None) and get_request.get('managed_service', None):
        query = '''
           profiles_userprofile.is_active = 1
           AND profiles_company.managed_service = 1
           '''
    elif get_request.get('active_users', None):
        query = '''
           profiles_userprofile.is_active = 1
           '''
    elif get_request.get('inactive_users', None) and get_request.get('managed_service', None):
        query = '''
           profiles_userprofile.is_active = 0
           AND profiles_company.managed_service = 1
           '''
    elif get_request.get('customer', None):
        query = '''
                 profiles_company.type IN ('Customer')
                 '''
    elif get_request.get('ex_customer', None):
        query = '''
                 profiles_company.type IN ('ex_customer')
                 '''
    elif get_request.get('inactive_users', None):
        query = '''
           profiles_userprofile.is_active = 0
           '''
    elif get_request.get('managed_service', None):
        query = '''
           profiles_company.managed_service = 1
           '''
    else:
        query = '''
            profiles_userprofile.is_active = 1
            '''
    return query

def export_extention(get_request):
    if get_request.get('all_users', None) and get_request.get('plan_users', None):
        list = get_request.getlist('plan_users', None)
        data =  "_".join(list)
    elif get_request.get('all_users', None) == "all_users":
        data = get_request.get('all_users', None)
    else:
        data = 'all_users'
    return data
