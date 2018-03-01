from django.core.management.base import BaseCommand
from tickets.models import Ticket
from profiles.models import UserProfile
from main.utils import send_mail, get_base_url
import datetime
from django.conf import settings
import logging
from main import settings

logger = logging.getLogger('emails')

class Command(BaseCommand):

    def handle(self, *args, **options):

        named_users = UserProfile.objects.filter(crm_type='named')
        open_tickets = []
        for user in named_users:
            tickets = Ticket.objects.filter(created_by=user, date_added__gte=datetime.datetime.now().replace(hour=0, minute=0, second=0)).exclude(assigned_to__isnull=True,status="closed",answers_no=0)
            for ticket in tickets:
                open_tickets.append(ticket)

        user = UserProfile.objects.get(email=settings.EMAIL_OF_REPORTING_PERSON)
        context = {
                'base_url': get_base_url(),
                'user': user,
                'open_tickets': open_tickets,
            }

        logger.info(u'Daily notification sent to staff {}'.format(user.email))

        send_mail(
            subject_template_name='emails/reminders/open_tickets_status_subject.txt',
            email_template_name='emails/reminders/open_tickets_status.txt',
            to_email=user.email,
            context=context,
            html_email_template_name='emails/reminders/open_tickets_status.html'
        )
