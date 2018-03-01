from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from main.utils import send_mail, get_base_url

from tickets.models import Ticket
from profiles.models import UserProfile
from profiles import constants

from connectors.sugarcrm import crm_interface

logger = logging.getLogger('emails')


class Command(BaseCommand):

    def handle(self, *args, **options):

        staff_users = UserProfile.objects.filter(
            is_active=True,
            crm_type__in=[constants.STAFF, constants.ADMIN, constants.MANAGER]
        )

        for user in staff_users:

            tickets = Ticket.objects.filter(
                assigned_to=user, is_deleted=False,
                status__in=['pending', 'inprogress', 'assigned']).order_by('date_modified')

            named_tickets = []
            community_tickets = []

            if not tickets:
                continue

            for ticket in tickets:

                if ticket.owned_by.is_named:

                    if not ticket.issue_type:
                        logger.error('Named ticket without issue type: {}'.format(ticket.id))

                    ticket.support_plan = crm_interface.get_support_plan(ticket.owned_by)

                    if not ticket.support_plan or not ticket.support_plan['support_plan']:
                        logger.error('Named ticket without support plan: {}'.format(ticket.id))

                    ticket.is_overdue = ticket.date_modified < timezone.now() - timedelta(days=10)

                    named_tickets.append(ticket)

                else:
                    community_tickets.append(ticket)

            context = {
                'base_url': get_base_url(),
                'user': user,
                'community_tickets': community_tickets,
                'named_tickets': named_tickets,
                'tickets_count': tickets.count()
            }

            logger.info(u'Daily digest sent to staff {}'.format(user.email))

            send_mail(
                subject_template_name='emails/reminders/staff_digest_subject.txt',
                email_template_name='emails/reminders/staff_digest.txt',
                to_email=user.email,
                context=context,
                html_email_template_name='emails/reminders/staff_digest.html',
                bcc=settings.DEFAULT_RECIPIENT_IDLE_TICKET_REMINDERS
            )
