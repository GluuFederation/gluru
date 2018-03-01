from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Ticket
from alerts.views import send_new_ticket_reminder_basic
from main.utils import log_emails


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('-notify_email', required=False)

    def handle(self, *args, **options):

        if options['notify_email']:
            notify_email = True
        else:
            notify_email = False

        tickets = Ticket.objects.filter(
            status__in=['new', 'assigned'],
            is_deleted=False, issue_type=''
        )

        for ticket in tickets:

            if not ticket.owned_by.is_basic:
                log_emails('New Ticket Reminder Basic: Ticket not owned by basic user {}'.format(
                    ticket.id), 'ERROR')
                continue

            if ticket.last_updated_at < timezone.now() - timedelta(hours=96):
                send_new_ticket_reminder_basic(ticket, notify_email)
