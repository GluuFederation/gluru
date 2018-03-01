from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import Client
from tickets.models import Ticket, Answer, TicketNotification
from profiles.models import UserProfile
from pytz import timezone
import datetime
from django.utils import timezone
import logging
from connectors.sugarcrm.crm_interface import get_support_plan
from tickets.utils import generate_ticket_link
from tickets.constants import ISSUE_TYPE, SMS_NUMBERS

logger = logging.getLogger('django')


class Command(BaseCommand):

    def handle(self, *arg, **option):
        try:
            tickets = Ticket.objects.filter(
                is_deleted=False, issue_type__in=['outage', 'impaired'],
                status__in=['pending', 'inprogress', 'assigned', 'new'], )
            account_sid = "Your twilio account sid"
            auth_token = "Your twilio auth token"
            client = Client(account_sid, auth_token)
            for ticket in tickets:
                support_plan = get_support_plan(ticket.created_by)
                if support_plan:
                    support_level = support_plan.get('support_plan')
                    if support_level == "Enterprise" and ticket.issue_type=="outage":
                        self.send_notification(5,ticket.issue_type,client,ticket)
                    elif support_level == "Premium" and ticket.issue_type=="outage":
                        self.send_notification(30,ticket.issue_type,client,ticket)
                    elif support_level == "Standard" and ticket.issue_type=="outage":
                        self.send_notification(60,ticket.issue_type,client,ticket)
                    elif support_level == "Basic" and ticket.issue_type=="outage":
                        self.send_notification(120,ticket.issue_type,client,ticket)
                    elif support_level == "Enterprise" and ticket.issue_type=="impaired":
                        self.send_notification(30,ticket.issue_type,client,ticket)
                    elif support_level == "Premium" and ticket.issue_type=="impaired":
                        self.send_notification(30,ticket.issue_type,client,ticket)
                    elif support_level == "Standard" and ticket.issue_type=="impaired":
                        self.send_notification(120,ticket.issue_type,client,ticket)
                    elif support_level == "Basic" and ticket.issue_type=="impaired":
                        self.send_notification(120,ticket.issue_type,client,ticket)
                    else:
                        continue
        except Exception as e:
            pass

    def send_notification (self,notification_send_time,issue_type,client,ticket):
        if ticket.date_added.date() == datetime.date.today():
            now = timezone.now()
            time_diff = now - ticket.date_added
            ticket_notification = self.check_notification_sent(ticket)
            if ticket_notification:

                if time_diff > datetime.timedelta(
                        minutes=notification_send_time) and not ticket_notification.is_txt_sent and not ticket_notification.is_try:
                    ticket_answer = Answer.objects.filter(ticket_id=ticket)

                    if not len(ticket_answer):
                        try:
                            for issue in ISSUE_TYPE:
                                if issue[0] == issue_type:
                                    issue_type = issue[1]

                            for sms in SMS_NUMBERS:
                                message = client.messages.create(

                                    to= sms[1],
                                    from_="Your contact number",
                                    body="Hello {0}, {1} from {2} has just opened a {3} on Gluu support:(https://support.gluu.org{4}). "
                                         "Please respond ASAP. "
                                         "Thanks! - Gluu Team".format(
                                        sms[0], ticket.created_by, ticket.company_association,
                                        issue_type, generate_ticket_link(ticket)
                                    )
                                )
                                if message.sid:
                                    log_message = 'SMS notification with ticket name:{} sent to staff member: {}'
                                    log_message = log_message.format(
                                        ticket.title , sms[0]
                                    )
                                    ticket_notification.is_try = 1
                                    ticket_notification.save()
                                    print "sms sent"

                        except Exception as e:
                            pass

    def check_notification_sent(self, ticket):
        try:
            result = TicketNotification.objects.get(ticket=ticket)
            return result
        except TicketNotification.DoesNotExist:
            return {}
