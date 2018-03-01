import logging
import json
import configparser
import os
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Sum
from profiles.models import UserProfile, Invitation, Company
from django.utils import timezone
from main.utils import send_mail, generate_sha1, log_emails, format_minutes
from main.utils import get_beginning_of_quarter

from connectors.idp.idp_interface import email_exists
from connectors.sugarcrm import crm_interface
from profiles import constants

logger = logging.getLogger('django')


def track_sent_emails(user, alert_type, emails):

    if not isinstance(emails, list):
        emails = [emails]

    log_message = 'Alert Sent: {}, User: {}, Recipient(s): {}, Added: {}'

    log_message = log_message.format(
        alert_type,
        user.id,
        emails,
        timezone.now()
    )

    log_emails(log_message)

def send_activation_email(user, key):

    activation_link = '{}://{}{}'.format(
        settings.PROTOCOL,
        Site.objects.get_current().domain,
        reverse('profile:activate', kwargs={'activation_key': key})
    )

    context = {
        'activation_link': activation_link,
        'name': user.first_name
    }

    send_mail(
        subject_template_name='emails/activate/verify_email_subject.txt',
        email_template_name='emails/activate/verify_email.txt',
        to_email=user.email,
        context=context,
        html_email_template_name='emails/activate/verify_email.html',
        bcc=settings.BCC
    )
    track_sent_emails(
        user=user,
        alert_type='activation_email',
        emails=[user.email,settings.BCC]
    )


def send_deactivation_email(user):

    send_mail(
        subject_template_name='emails/deactivate/deactivate_named_user_subject.txt',
        email_template_name='emails/deactivate/deactivate_named_user.txt',
        to_email=user.email,
        context={},
        html_email_template_name='emails/deactivate/deactivate_named_user.html'
    )
    track_sent_emails(
        user=user,
        alert_type='deactivation_email',
        emails=user.email
    )

def send_revoke_access_email(user, company):

    send_mail(
        subject_template_name='emails/deactivate/revoke_access_named_subject.txt',
        email_template_name='emails/deactivate/revoke_access_named.txt',
        to_email=user.email,
        context={'company': company},
        html_email_template_name='emails/deactivate/revoke_access_named.html'
    )
    track_sent_emails(
        user=user,
        alert_type='send_revoke_access_email',
        emails=user.email
    )

def send_new_user_notification(user):

    site = Site.objects.get_current()

    context = {
        'site_name': site.name,
        'user': user
    }

    send_mail(
        subject_template_name='emails/new_user/new_user_subject.txt',
        email_template_name='emails/new_user/new_user.txt',
        to_email=settings.USER_MANAGEMENT_EMAIL,
        context=context,
        html_email_template_name='emails/new_user/new_user.html',
        bcc=settings.BCC
    )
    track_sent_emails(
        user=user,
        alert_type='send_new_user_notification',
        emails=[settings.USER_MANAGEMENT_EMAIL,settings.BCC]
    )


def send_activate_account_notification(user):

    context = {
        'company': user.company,
        'user': user
    }

    send_mail(
        subject_template_name='emails/activate/activate_email_subject.txt',
        email_template_name='emails/activate/activate_email.txt',
        to_email=user.email,
        context=context,
        html_email_template_name='emails/activate/activate_email.html',
        bcc=settings.BCC
    )
    track_sent_emails(
        user=user,
        alert_type='send_activate_account_notification',
        emails=[user.email,settings.BCC]
    )

def send_invitation(invitation):

    existing = email_exists(invitation.email)

    if existing:

        invitation_link = '{}://{}{}?next={}'.format(
            settings.PROTOCOL,
            Site.objects.get_current().domain,
            reverse('social:begin', args=['gluu']),
            reverse('profile:accept-invite', kwargs={'activation_key': invitation.activation_key})
        )

    else:

        invitation_link = '{}://{}{}'.format(
            settings.PROTOCOL,
            Site.objects.get_current().domain,
            reverse('profile:register-named', kwargs={'activation_key': invitation.activation_key}),
        )

    context = {
        'name': invitation.invited_by.get_full_name(),
        'invited_by': invitation.invited_by.get_full_name(),
        'company': invitation.invited_by.company_association.name,
        'invitation_link': invitation_link,
        'existing': existing
    }
    try:
        account = UserProfile.objects.get(email=invitation.email)
        if (account.first_name != ""):
            context['fname'] = account.first_name
    except UserProfile.DoesNotExist:
        pass
    send_mail(
        subject_template_name='emails/invite/invite_named_subject.txt',
        email_template_name='emails/invite/invite_named.txt',
        to_email=invitation.email,
        context=context,
        html_email_template_name='emails/invite/invite_named.html',
        bcc=settings.BCC
    )
    log_emails(
        u'Alert Sent: send_invitation, Recipient(s): {}, Added: {}'.format(invitation.email,timezone.now())
    )

def send_account_admin_notification(user, invited_by):

    context = {
        'name': user.first_name,
        'company': user.get_company(),
    }

    send_mail(
        subject_template_name='emails/promotion/role_admin_subject.txt',
        email_template_name='emails/promotion/role_admin.txt',
        to_email=user.email,
        context=context,
        html_email_template_name='emails/promotion/role_admin.html'
    )
    track_sent_emails(
        user=user,
        alert_type='send_account_admin_notification',
        emails=user.email
    )

def send_role_change_notification(user, current_role, deactivated=False):

    context = {
        'user': user,
        'current_role': current_role,
        'deactivated': deactivated,
        'company': user.get_company()
    }

    if deactivated:
        context['new_role'] = 'inactive'
    elif user.is_company_admin:
        context['new_role'] = 'admin'
    elif user.is_named:
        context['new_role'] = 'named'
    else:
        context['new_role'] = 'community'

    send_mail(
        subject_template_name='emails/promotion/role_admin_subject.txt',
        email_template_name='emails/promotion/role_admin.txt',
        to_email=user.email,
        context=context,
        html_email_template_name='emails/promotion/role_admin.html',
        bcc=settings.RECIPIENT_NEW_NOTIFICATIONS
    )
    track_sent_emails(
        user=user,
        alert_type='send_role_change_notification',
        emails=[user.email,settings.RECIPIENT_NEW_NOTIFICATIONS]
    )

def send_revoke_account_admin_notification(user):

    context = {'company': user.get_company()}

    send_mail(
        subject_template_name='emails/deactivate/revoke_access_admin_subject.txt',
        email_template_name='emails/deactivate/revoke_access_admin.txt',
        to_email=user.email,
        context=context,
        html_email_template_name='emails/deactivate/revoke_access_admin.html'
    )
    track_sent_emails(
        user=user,
        alert_type='send_revoke_account_admin_notification',
        emails=user.email
    )

def send_new_partner_notification(partner, client, company_admin):

    company_members = partner.named_users.all().values_list('email', flat=True)

    to_emails = [c for c in company_members]

    context = {
        'company': client.name,
        'company_admin': company_admin
    }

    send_mail(
        subject_template_name='emails/partnership/new_partnership_subject.txt',
        email_template_name='emails/partnership/new_partnership.txt',
        to_email=to_emails,
        context=context,
        html_email_template_name='emails/partnership/new_partnership.html'
    )
    log_emails(
        u'Alert Sent: send_new_partner_notification, Recipient(s): {}, Added: {}'.format(to_emails,timezone.now())
    )

def send_partnership_revoked_notification(partner, client, company_admin):

    company_members = partner.named_users.all().values_list('email', flat=True)

    to_emails = [c for c in company_members]

    context = {
        'company': client.name,
        'company_admin': company_admin
    }

    send_mail(
        subject_template_name='emails/partnership/partnership_revoked_subject.txt',
        email_template_name='emails/partnership/partnership_revoked.txt',
        to_email=to_emails,
        context=context,
        html_email_template_name='emails/partnership/partnership_revoked.html'
    )
    log_emails(
            u'Alert Sent: send_partnership_revoked_notification, Recipient(s): {}, Added: {}'.format( to_emails,timezone.now())
    )

def generate_activation_key(email):

    _, activation_key = generate_sha1(email)
    return activation_key


def create_invite(email, invited_by):

    invitations = Invitation.objects.filter(email=email).exclude(
        activation_key__in=['REVOKED', 'ACTIVATED', 'EXPIRED'])

    if len(invitations) > 1:
        logger.error('More than one active invite for email {}'.format(email))

    elif len(invitations) == 1:
        invitations[0].activation_key = 'EXPIRED'
        invitations[0].save()

    activation_key = generate_activation_key(email)

    invitation = Invitation(
        email=email,
        invited_by=invited_by,
        activation_key=activation_key
    )

    invitation.save()

    send_invitation(invitation)


def notify_company_admin(new_user):

    company_emails = UserProfile.objects.filter(is_company_admin=True).values_list('email', flat=True)
    email_suffixes = {email.split('@')[1]: email for email in company_emails}

    if new_user.email.split('@')[1] in email_suffixes.keys() and new_user.email.split('@')[1] not in ['gmail.com', 'yahoo.com', 'hotmail.com']:

        to_email = email_suffixes[new_user.email.split('@')[1]]
        admin = UserProfile.objects.get(email=to_email)

        send_mail(
            subject_template_name='emails/new_user/new_user_company_admin_subject.txt',
            email_template_name='emails/new_user/new_user_company_admin.txt',
            to_email=to_email,
            context={'user': new_user, 'admin': admin},
            html_email_template_name='emails/new_user/new_user_company_admin.html',
            bcc=settings.BCC
        )

        log_emails(
            u'Alert Sent: Notify Company Admin about new user, New user: {}, Admin: {}, Added: {}'.format(new_user, to_email,timezone.now()))


def get_support_details(request):

        if request.user.is_named:
            company = request.user.company_association
            support_plan = crm_interface.get_support_plan(request.user)
            if support_plan:
                cmp = Company.objects.get(id=company.id)
                if cmp.entitlements != "[]":
                    response= json.loads(cmp.entitlements)
                    available_support_time = response['support_hours']
                    available_review_time = response['review_hours']
                    support_plan['named_contacts'] = response['named_contacts']

                support_plan['available_support_time'] = available_support_time
                support_plan['available_review_time'] = available_review_time

                support_plan['remaining_support_time'] = format_minutes(
                    (available_support_time * 60) -
                    get_spent_meeting_minutes(company, 'SUP', support_plan['start_date'])
                )

                support_plan['remaining_review_time'] = format_minutes(
                    (available_review_time * 60) -
                    get_spent_meeting_minutes(company, 'REV', support_plan['start_date'])
                )

                return support_plan
            else:
                return []
        else:
            return []

def get_spent_meeting_minutes(company, meeting_type, start_date):

    beginning_quarter = get_beginning_of_quarter(start_date)

    spent = company.meetings.filter(
        meeting_type=meeting_type,
        date__gt=beginning_quarter
    ).aggregate(Sum('duration_in_minutes'))['duration_in_minutes__sum']

    if spent:
        return spent
    else:
        return 0

def oxd_cfg_file_data():
    config = configparser.ConfigParser()
    this_dir = os.path.dirname(os.path.realpath(__file__))
    config_location = os.path.join(this_dir, 'gluu.cfg')
    config.read(config_location)
    data = []
    data.append(config.get('oxd','host'))
    data.append(config.get('oxd','port'))
    data.append(config.get('oxd','id'))
    data.append(config.get('client','op_host'))
    data.append(config.get('client','authorization_redirect_uri'))
    data.append(config.get('client','post_logout_redirect_uri'))
    data.append(config.get('client','scope'))
    data.append(config.get('client','client_id'))
    data.append(config.get('client','client_secret'))
    data.append(config.get('client','grant_types'))
    data.append(config.get('client','client_id_issued_at'))
    return data
