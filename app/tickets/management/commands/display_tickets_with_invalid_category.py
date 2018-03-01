from django.core.management.base import BaseCommand

from tickets.models import Ticket
from tickets.constants import TICKET_CATEGORY

from tickets.utils import generate_ticket_link
from main.utils import log_error


class Command(BaseCommand):

    def handle(self, *args, **options):

        categories = [c[0] for c in TICKET_CATEGORY]

        tickets = Ticket.objects.filter(is_deleted=False)
        for ticket in tickets:
            if ticket.ticket_category not in categories:
                log_error('{} {} {}'.format(ticket.id, ticket.ticket_category, generate_ticket_link(ticket)))
                ticket.ticket_category = ticket.ticket_category.upper()
                ticket.save()
