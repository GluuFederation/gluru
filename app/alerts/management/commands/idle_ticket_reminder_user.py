from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Ticket
from alerts.views import send_idle_ticket_reminder_user


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('-notify_email', required=False)

    def handle(self, *args, **options):

        if options['notify_email']:
            notify_email = True
        else:
            notify_email = False

        tickets = Ticket.objects.filter(status='pending', is_deleted=False)

        for ticket in tickets:

            if not ticket.modified_by or not ticket.modified_by.is_admin:
                continue

            if ticket.last_updated_at < timezone.now() - timedelta(days=5):
                send_idle_ticket_reminder_user(ticket, notify_email)
