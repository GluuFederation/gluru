from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template import loader
from django.utils import timezone
from connectors.sugarcrm.crm_interface import get_support_plan
from tickets.models import TicketAlerts
from main.utils import send_mail, get_base_url, log_emails, format_timedelta, send_email
from tickets.utils import generate_ticket_link
from BeautifulSoup import BeautifulSoup
from django.http import Http404, HttpResponseRedirect, HttpResponse
import markdown
import requests
import base64
from alerts.constants import test_emails

NEW_TICKET = 'new_ticket'
NEW_TICKET_FOR_USER = 'new_ticket_for_user'
NEW_TICKET_BY_STAFF = 'new_ticket_by_staff'
NEW_TICKET_BY_NAMED = 'new_ticket_by_named'
NEW_TICKET_FOR_NAMED = 'new_ticket_for_named'
NEW_TICKET_COPY = 'copy_ticket'
TICKET_REOPENED = 'ticket_reopened'

TICKET_ASSIGNED = 'assigned_ticket'
TICKET_ASSIGNED_OWNER = 'assigned_ticket_owner'

NEW_ANSWER = 'new_answer'
NEW_ANSWER_SUBSCRIBERS = 'new_answer_subscribers'
NEW_ANSWER_COPY = 'copy_answer'
NEW_ANSWER_TAGGED_STAFF_MEMBER = 'new_answer_tagged_staff_member'

def generate_ticket_url(ticket):

    url = generate_ticket_link(ticket)
    return '{}{}'.format(get_base_url(), url)


def generate_unubscribe_link(ticket):

    url = reverse('ticket_blacklist', kwargs={'id': ticket.id})

    return '{}{}'.format(get_base_url(), url)


def generate_subscribe_link(ticket):

    url = reverse('ticket_add_alert', kwargs={'id': ticket.id})

    return '{}{}'.format(get_base_url(), url)


def get_staff_involved(ticket):

    recipients = []

    if ticket.assigned_to:
        recipients.append(ticket.assigned_to)

    if ticket.created_by != ticket.owned_by and ticket.created_by.is_admin:
        recipients.append(ticket.created_by)

    ticket_alerts = ticket.ticket_alerts.filter(
        ticket=ticket,
        user__is_active=True,
        user__crm_type__in=['staff', 'admin', 'manager']
    )

    for alert in ticket_alerts:
        recipients.append(alert.user)

    blacklisted_users = [item.user for item in ticket.blacklist.all()]

    return list(set(recipients) - set(blacklisted_users))


def send_new_ticket_reminder(ticket, support_plan, notify_email=False):

    context = {
        'ticket': ticket,
        'ticket_link': generate_ticket_url(ticket),
        'support_plan': support_plan
    }

    log_message = 'New Ticket Reminder to Staff Sent, Ticket: {}, Support Plan: {}, Issue Type: {}, Time passed: {}'

    log_emails(log_message.format(
        ticket.id, support_plan, ticket.issue_type, timezone.now() - ticket.last_updated_at
    ))

    if notify_email:

        send_email(
            subject_template_name='emails/reminders/new_ticket_reminder_subject.txt',
            email_template_name='emails/reminders/new_ticket_reminder.txt',
            to_email=settings.RECIPIENT_NEW_NOTIFICATIONS,
            context=context,
            html_email_template_name='emails/reminders/new_ticket_reminder.html',
            bcc=settings.DEFAULT_RECIPIENT_IDLE_TICKET_REMINDERS
        )

        ticket.last_notification_sent = timezone.now()
        ticket.save()


def send_new_ticket_reminder_basic(ticket, notify_email=False):

    context = {
        'ticket': ticket,
        'ticket_link': generate_ticket_url(ticket)
    }

    log_message = 'New Ticket Reminder for community user to Staff Sent, Ticket: {}, Time passed: {}'

    log_emails(log_message.format(ticket.id, timezone.now() - ticket.last_updated_at))

    if notify_email:

        send_email(
            subject_template_name='emails/reminders/new_ticket_reminder_basic_subject.txt',
            email_template_name='emails/reminders/new_ticket_reminder_basic.txt',
            to_email=settings.RECIPIENT_NEW_NOTIFICATIONS,
            context=context,
            html_email_template_name='emails/reminders/new_ticket_reminder_basic.html',
            bcc=settings.DEFAULT_RECIPIENT_IDLE_TICKET_REMINDERS
        )

        ticket.last_notification_sent = timezone.now()
        ticket.save()


def send_idle_ticket_reminder_user(ticket, notify_email=False):

    context = {
        'ticket': ticket,
        'ticket_link': generate_ticket_url(ticket),
        'time_passed': format_timedelta(timezone.now() - ticket.date_modified),
        'unsubscribe_link': generate_unubscribe_link(ticket),
        'close_ticket_link': '{}{}'.format(get_base_url(), reverse('close_ticket', kwargs={'id': ticket.id}))
    }

    log_message = u'Idle Ticket Reminder to User Sent, Ticket: {}, Recipient: {}, Time passed: {}'

    log_emails(log_message.format(ticket.id, ticket.owned_by, timezone.now() - ticket.last_updated_at))

    if notify_email:

        send_email(
            subject_template_name='emails/reminders/idle_ticket_reminder_user_subject.txt',
            email_template_name='emails/reminders/idle_ticket_reminder_user.txt',
            to_email=ticket.owned_by.email,
            context=context,
            html_email_template_name='emails/reminders/idle_ticket_reminder_user.html',
            bcc=settings.DEFAULT_RECIPIENT_IDLE_TICKET_REMINDERS
        )

        ticket.last_notification_sent = timezone.now()
        ticket.save()


def gather_ticket_email_context(ticket):

    site = Site.objects.get_current()

    html = markdown.markdown(ticket.description, safe_mode='escape', extensions=['markdown.extensions.fenced_code'])
    text = ''.join(BeautifulSoup(html).findAll(text=True))

    context = {
        'ticket_id': ticket.id,
        'ticket_title': ticket.title,
        'site_name': site.name,
        'ticket_link': generate_ticket_url(ticket),
        'ticket_created_by': ticket.created_by,
        'ticket_created_by_comp': ticket.created_by.get_company(),
        'ticket_body': markdown.markdown(ticket.description, safe_mode='escape', extensions=['markdown.extensions.fenced_code']),
        'ticket_body_txt': text,
        'subscription_link': generate_subscribe_link(ticket),
        'issue_type': ticket.issue_type
    }

    if ticket.support_plan:
        support_plan = ticket.support_plan.get('support_plan')
        if support_plan != 'blank':
            context['support_plan'] = support_plan
        if ticket.issue_type == 'Production Outage':
            if support_plan == 'Basic':
                context['hours'] = 'Customer SLA: 12 hours.'
            elif support_plan == 'Premium':
                context['hours'] = "Customer SLA: 2 hours."
            elif support_plan == 'Enterprise':
                context['hours'] = "Customer SLA: 1 hour."
            elif support_plan == 'Standard':
                context['hours'] = "Customer SLA: 3 hours."
        if ticket.issue_type == 'Production Impaired':
            if support_plan == 'Basic':
                context['hours'] = 'Customer SLA: 1 bus. day.'
            elif support_plan == 'Premium':
                context['hours'] = "Customer SLA: 4 hours."
            elif support_plan == 'Enterprise':
                context['hours'] = "Customer SLA: 4 hours."
            elif support_plan == 'Standard':
                context['hours'] = "Customer SLA: 6 hours."
        if ticket.issue_type == 'Pre-Production Issue':
            if support_plan == 'Basic':
                context['hours'] = 'Customer SLA: 1 bus. day.'
            elif support_plan == 'Premium':
                context['hours'] = "Customer SLA: 12 hours."
            elif support_plan == 'Enterprise':
                context['hours'] = "Customer SLA: 12 hours."
            elif support_plan == 'Standard':
                context['hours'] = "Customer SLA: 1 bus. day."
        if ticket.issue_type == 'Minor Issue':
            if support_plan == 'Basic':
                context['hours'] = 'Customer SLA: 1 bus. day.'
            elif support_plan == 'Premium':
                context['hours'] = "Customer SLA: 1 bus. day."
            elif support_plan == 'Enterprise':
                context['hours'] = "Customer SLA: 1 bus. day."
            elif support_plan == 'Standard':
                context['hours'] = "Customer SLA: 1 bus. day."
        if ticket.issue_type == 'New Development Issue':
            if support_plan == 'Basic':
                context['hours'] = 'Customer SLA: 3 bus. days.'
            elif support_plan == 'Premium':
                context['hours'] = "Customer SLA: 2 bus. days."
            elif support_plan == 'Enterprise':
                context['hours'] = "Customer SLA: 2 bus. days."
            elif support_plan == 'Standard':
                context['hours'] = "Customer SLA: 1 bus. day."

    if ticket.created_for:
        context['ticket_created_for'] = ticket.created_for
        context['ticket_created_for_comp'] = ticket.created_for.get_company()

    return context


def gather_answer_email_context(answer):

    site = Site.objects.get_current()
    if answer.created_by.company == 'Gluu':
        support_plan = "Staff"
    else:
        plan = get_support_plan(answer.created_by)
        if not plan or not plan['support_plan']:
            support_plan = "Community"
        else:
            support_plan = plan['support_plan']
    ticket_link = '{}#at{}'.format(generate_ticket_url(answer.ticket), answer.id)

    context = {
        'site_name': site.name,
        'ticket_id': answer.ticket.id,
        'ticket_title': answer.ticket.title,
        'support_plan': support_plan,
        'ticket_link': ticket_link,
        'answer_created_by': answer.created_by,
        'answer_created_by_comp': answer.created_by.get_company(),
        'answer_body': answer.answer,
        'subscription_link': generate_subscribe_link(answer.ticket)
    }

    return context


def track_sent_emails(ticket, alert_type, emails):

    if not isinstance(emails, list):
        emails = [emails]

    log_message = 'Alert Sent: {}, Ticket: {}, Recipient(s): {}, Added: {}'

    log_message = log_message.format(
        alert_type,
        ticket.id,
        emails,
        timezone.now()
    )

    log_emails(log_message)


def notify_new_ticket(ticket, send_copy=False):

    context = gather_ticket_email_context(ticket)
    encoded= base64.b32encode(str(ticket.id))
    # test_emails.append(settings.RECIPIENT_NEW_NOTIFICATIONS)

    if ticket.created_for:

        send_email(
            subject_template_name='emails/new_ticket/new_ticket_subject.txt',
            email_template_name='emails/new_ticket/new_ticket_for_user.txt',
            to_email=ticket.created_for.email,
            context=context,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>" ,
            html_email_template_name='emails/new_ticket/new_ticket_for_user.html'
        )

        send_email(
            subject_template_name='emails/new_ticket/new_ticket_subject.txt',
            email_template_name='emails/new_ticket/new_ticket_for_staff.txt',
            to_email=test_emails,
            context=context,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>" ,
            html_email_template_name='emails/new_ticket/new_ticket_for_staff.html'
        )

        track_sent_emails(
            ticket=ticket,
            alert_type=NEW_TICKET_FOR_USER,
            emails=[ticket.created_for.email, test_emails]
        )

        if ticket.created_for.is_named:

            if ticket.created_by.get_company() == 'Gluu':
                company_members_creator = []
            else:
                company_members_creator = ticket.created_by.company_association.named_users.filter(is_active=True, receive_all_notifications=True).exclude(
                    email=ticket.created_by.email).values_list('email', 'first_name')

            all_mambers = []

            for member in company_members_creator:
                all_mambers.append([member[0], member[1]])

            company_members_owner = ticket.created_for.company_association.named_users.filter(is_active=True, receive_all_notifications=True).exclude(
                email=ticket.created_for.email).values_list('email', 'first_name')

            for member in company_members_owner:
                all_mambers.append([member[0], member[1]])

            if all_mambers:
                for item in all_mambers:
                    context['named_user_name'] = item[1]
                    send_email(
                        subject_template_name='emails/new_ticket/new_ticket_subject.txt',
                        email_template_name='emails/new_ticket/new_ticket_for_named.txt',
                        to_email=item[0],
                        from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                        context=context,
                        html_email_template_name='emails/new_ticket/new_ticket_for_named.html'
                    )

                    track_sent_emails(
                        ticket=ticket,
                        emails=item[0],
                        alert_type=NEW_TICKET_FOR_NAMED
                    )

    else:

        if ticket.created_by.is_admin:

            send_email(
                subject_template_name='emails/new_ticket/new_ticket_subject.txt',
                email_template_name='emails/new_ticket/new_ticket_by_staff.txt',
                to_email=test_emails,
                context=context,
                from_email = "From Title <"+encoded+ "@your domain on mailgun>" ,
                html_email_template_name='emails/new_ticket/new_ticket_by_staff.html'
            )

            track_sent_emails(
                ticket=ticket,
                alert_type=NEW_TICKET_BY_STAFF,
                emails=[test_emails]
            )

        if ticket.created_by.is_basic:
            send_email(
                subject_template_name='emails/new_ticket/new_ticket_subject.txt',
                email_template_name='emails/new_ticket/new_ticket.txt',
                to_email='To email will go here',
                from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                context=context,
                html_email_template_name='emails/new_ticket/new_ticket.html'
            )
            send_email(
                subject_template_name='emails/new_ticket/thank_you_note_subject.txt',
                email_template_name='emails/new_ticket/new_ticket_note_for_user.txt',
                to_email='To email will go here',
                from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                context=context,
                html_email_template_name='emails/new_ticket/new_ticket_note_for_user.html'
            )

            track_sent_emails(
                ticket=ticket,
                alert_type=NEW_TICKET,
                emails=test_emails
            )

        elif ticket.created_by.is_named:

            company = ticket.created_by.company_association
            context['ticket_created_by_comp'] = ticket.created_by.company_association.name

            send_email(
                subject_template_name='emails/new_ticket/new_ticket_subject.txt',
                email_template_name='emails/new_ticket/new_ticket_by_named.txt',
                to_email=test_emails,
                from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                context=context,
                html_email_template_name='emails/new_ticket/new_ticket_by_named.html'

            )

            send_email(
                subject_template_name='emails/new_ticket/thank_you_note_subject.txt',
                email_template_name='emails/new_ticket/new_ticket_note_for_named.txt',
                to_email='To email will go here',
                from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                context=context,
                html_email_template_name='emails/new_ticket/new_ticket_note_for_named.html'
            )

            track_sent_emails(
                ticket=ticket,
                emails=test_emails,
                alert_type=NEW_TICKET_BY_NAMED
            )

            company_members = company.named_users.filter(is_active=True, receive_all_notifications=True).exclude(
                email=ticket.created_by.email).values_list('email', 'first_name')

            if company_members:
                for item in company_members:
                    context['named_user_name'] = item[1]
                    send_email(
                        subject_template_name='emails/new_ticket/new_ticket_subject.txt',
                        email_template_name='emails/new_ticket/new_ticket_for_named.txt',
                        from_email = "From Title <"+encoded+ "@your domain on mailgun>",
                        to_email=item[0],
                        context=context,
                        html_email_template_name='emails/new_ticket/new_ticket_for_named.html'
                    )

                    track_sent_emails(
                        ticket=ticket,
                        emails=item[0],
                        alert_type=NEW_TICKET_BY_NAMED
                    )

    if send_copy:

        to_emails = [e.strip() for e in ticket.send_copy.split(',')]

        send_email(
            subject_template_name='emails/new_ticket/new_ticket_copy_subject.txt',
            email_template_name='emails/new_ticket/new_ticket_copy.txt',
            to_email=to_emails,
            context=context,
            html_email_template_name='emails/new_ticket/new_ticket_copy.html',
            from_email = "From Title <"+encoded+ "@your domain on mailgun>"
        )

        track_sent_emails(
            ticket=ticket,
            emails=test_emails,
            alert_type=NEW_TICKET_COPY
        )


def notify_ticket_reopened(ticket, user):

    context = gather_ticket_email_context(ticket)
    context['ticket_reopened_by'] = user
    context['ticket_reopened_by_comp']=user.get_company()

    to_emails = test_emails.append(settings.RECIPIENT_NEW_NOTIFICATIONS)

    if ticket.assigned_to and ticket.assigned_to != user:
        to_emails.append(ticket.assigned_to.email)

    send_email(
        subject_template_name='emails/new_ticket/ticket_reopened_subject.txt',
        email_template_name='emails/new_ticket/ticket_reopened.txt',
        to_email=to_emails,
        context=context,
        html_email_template_name='emails/new_ticket/ticket_reopened.html',
    )

    track_sent_emails(
        ticket=ticket,
        emails=to_emails,
        alert_type=TICKET_REOPENED
    )


def notify_ticket_assigned(ticket, user):

    context = gather_ticket_email_context(ticket)
    encoded= base64.b32encode(str(ticket.id))
    context['ticket_assigned_by'] = user
    context['ticket_assigned_to'] = ticket.assigned_to
    context['first_name']=ticket.assigned_to.get_short_name

    if ticket.assigned_to != user:

        send_email(
            subject_template_name='emails/ticket_assigned/ticket_assigned_subject.txt',
            email_template_name='emails/ticket_assigned/ticket_assigned.txt',
            to_email=ticket.assigned_to.email,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>",
            context=context,
            html_email_template_name='emails/ticket_assigned/ticket_assigned.html'
        )

        track_sent_emails(
            ticket=ticket,
            emails=ticket.assigned_to.email,
            alert_type=TICKET_ASSIGNED
        )

    if ticket.assigned_first_time and ticket.owned_by != user and ticket.created_by.is_named:

        send_email(
            subject_template_name='emails/ticket_assigned/ticket_assigned_to_creator_subject.txt',
            email_template_name='emails/ticket_assigned/ticket_assigned_to_creator.txt',
            to_email=ticket.owned_by.email,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>",
            context=context,
            html_email_template_name='emails/ticket_assigned/ticket_assigned_to_creator.html'
        )

        track_sent_emails(
            ticket=ticket,
            emails=ticket.owned_by.email,
            alert_type=TICKET_ASSIGNED_OWNER
        )


def notify_new_answer(answer, send_copy=False):

    ticket = answer.ticket
    encoded= base64.b32encode(str(ticket.id))
    context = gather_answer_email_context(answer)

    to_emails = []

    if answer.created_by != ticket.owned_by and ticket.owned_by.is_active:

        to_emails.append(ticket.owned_by.email)

    if (ticket.assigned_to and answer.created_by != ticket.assigned_to and
            ticket.assigned_to.is_active):

        to_emails.append(ticket.assigned_to.email)

    if to_emails:

        send_email(
            subject_template_name='emails/new_answer/new_answer_subject.txt',
            email_template_name='emails/new_answer/new_answer.txt',
            to_email=to_emails,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>",
            context=context,
            html_email_template_name='emails/new_answer/new_answer.html',
        )

        track_sent_emails(
            ticket=ticket,
            emails=to_emails,
            alert_type=NEW_ANSWER
        )

    excluded_subscribers = [answer.created_by.email, ticket.owned_by.email]

    if ticket.assigned_to:
        excluded_subscribers.append(ticket.assigned_to.email)

    ticket_alerts = TicketAlerts.objects.filter(
        ticket=answer.ticket, user__is_active=True).exclude(
        user__email__in=excluded_subscribers
    )

    to_emails = [alert.user.email for alert in ticket_alerts]
    to_emails = list(set(to_emails))

    if ticket.company_association:

        company = ticket.company_association

        subscribed_company_members = company.named_users.filter(
            is_active=True, receive_all_notifications=True).exclude(
            email__in=excluded_subscribers)

        subscribed_company_members = [user.email for user in subscribed_company_members]

        to_emails = list(set(to_emails) | set(subscribed_company_members))

    if to_emails:

        send_email(
            subject_template_name='emails/new_answer/new_answer_subject.txt',
            email_template_name='emails/new_answer/new_answer_subscriber.txt',
            to_email=to_emails,
            from_email = "From Title <"+encoded+ "@your domain on mailgun>",
            context=context,
            html_email_template_name='emails/new_answer/new_answer_subscriber.html',
        )

        track_sent_emails(
            ticket=ticket,
            emails=to_emails,
            alert_type=NEW_ANSWER_SUBSCRIBERS
        )

    if send_copy:

        to_emails = [e.strip() for e in answer.send_copy.split(',')]

        send_email(
            subject_template_name='emails/new_answer/new_answer_copy_subject.txt',
            email_template_name='emails/new_answer/new_answer_copy.txt',
            to_email=to_emails,
            context=context,
            html_email_template_name='emails/new_answer/new_answer_copy.html',
            from_email = "From Title <"+encoded+ "@your domain on mailgun>"
        )

        track_sent_emails(
            ticket=ticket,
            emails=to_emails,
            alert_type=NEW_ANSWER_COPY
        )

def notify_tagged_staff_member(answer, tag_user):

    ticket = answer.ticket
    encoded= base64.b32encode(str(ticket.id))
    context = gather_answer_email_context(answer)

    send_email(
        subject_template_name='emails/new_answer/new_answer_tagged_staff_member_subject.txt',
        email_template_name='emails/new_answer/new_answer_tagged_staff_member.txt',
        to_email=To email will go here,
        context=context,
        html_email_template_name='emails/new_answer/new_answer_tagged_staff_member.html',
        from_email = "From Title <"+encoded+ "@your domain on mailgun>"
    )

    track_sent_emails(
        ticket=ticket,
        emails=tag_user.email,
        alert_type=NEW_ANSWER_TAGGED_STAFF_MEMBER
    )
