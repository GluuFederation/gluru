import logging
from django.core.management.base import BaseCommand

from tickets.models import Ticket

logger = logging.getLogger('django')


class Command(BaseCommand):

    def handle(self, *args, **options):

        tickets = Ticket.objects.filter(is_deleted=False)

        for ticket in tickets:

            if ticket.owned_by.company_association:

                ticket.company_association = ticket.owned_by.company_association
                logger.info(u'Added company {} to ticket {}'.format(
                    ticket.owned_by.company_association, ticket.id))
                ticket.save()

            elif not ticket.owned_by.is_basic:

                logger.error(u'{} without company association'.format(ticket.owned_by.email))
