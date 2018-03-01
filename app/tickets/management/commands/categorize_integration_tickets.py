from django.core.management.base import BaseCommand

from tickets.models import Ticket

from main.utils import log_error


class Command(BaseCommand):

    def handle(self, *args, **options):

        tickets = Ticket.objects.filter(is_deleted=False)
        count = 0
        for ticket in tickets:
            if ticket.ticket_category.strip().upper() == 'INTEGRATIONS':

                if 'SCIM' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category IDNTY assigned'.format(ticket.id))
                    ticket.ticket_category = 'IDNTY'
                    ticket.save()
                elif 'UMA' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category ACCESS assigned'.format(ticket.id))
                    ticket.ticket_category = 'ACCESS'
                    ticket.save()
                elif 'SAML' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category SSO assigned'.format(ticket.id))
                    ticket.ticket_category = 'SSO'
                    ticket.save()
                elif 'OPENID' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category SSO assigned'.format(ticket.id))
                    ticket.ticket_category = 'SSO'
                    ticket.save()
                elif 'SSO' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category SSO assigned'.format(ticket.id))
                    ticket.ticket_category = 'SSO'
                    ticket.save()
                elif 'LDAP' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category IDNTY assigned'.format(ticket.id))
                    ticket.ticket_category = 'IDNTY'
                    ticket.save()
                elif 'SHIBBOLETH' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category SSO assigned'.format(ticket.id))
                    ticket.ticket_category = 'SSO'
                    ticket.save()
                elif 'ASIMBA' in ticket.title.upper():
                    count = count + 1
                    log_error('Ticket {} got category SSO assigned'.format(ticket.id))
                    ticket.ticket_category = 'SSO'
                    ticket.save()

        log_error('Assigned {} tickets'.format(count))
