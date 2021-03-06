from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Ticket
from connectors.sugarcrm.crm_interface import get_support_plan
from alerts.views import send_new_ticket_reminder
from main.utils import log_emails

from alerts.constants import SLA_MATRIX_NEW


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('-notify_email', required=False)

    def handle(self, *args, **options):

        if options['notify_email']:
            notify_email = True
        else:
            notify_email = False

        tickets = Ticket.objects.filter(
            status__in=['new', 'assigned'], is_deleted=False).exclude(
            issue_type='outage').exclude(issue_type='')

        for ticket in tickets:

            if ticket.owned_by.is_admin:
                continue

            if ticket.owned_by.is_basic:
                log_emails('New Ticket Reminder: Ticket with issue type by basic user {}'.format(
                    ticket.id), 'ERROR')
                continue

            support_plan = get_support_plan(ticket.owned_by)

            if not support_plan or not support_plan['support_plan']:
                log_emails('New Ticket Reminder: No support plan found for {}'.format(
                    ticket.owned_by.get_company()), 'ERROR')
                continue

            sla_time_delta = SLA_MATRIX_NEW[support_plan['support_plan']][ticket.issue_type]

            if ticket.last_updated_at < timezone.now() - timedelta(hours=sla_time_delta):
                send_new_ticket_reminder(ticket, support_plan['support_plan'], notify_email)
