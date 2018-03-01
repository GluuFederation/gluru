from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import Company
from profiles.constants import SUPPORT_PLAN_2_NO_NAMED_CONTACTS,REVIEW_HOURS_PER_QUARTER,SUPPORT_HOURS_PER_QUARTER
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        company = Company.objects.all()

        for c in company:
           data = {}
           if c.support_plan == 'Basic':
               data["named_contacts"] = SUPPORT_PLAN_2_NO_NAMED_CONTACTS[c.support_plan]
               data["review_hours"] = REVIEW_HOURS_PER_QUARTER[c.support_plan]
               data["support_hours"] = SUPPORT_HOURS_PER_QUARTER[c.support_plan]
               f_data = json.dumps(data)
           elif c.support_plan == 'Standard':
               data["named_contacts"] = SUPPORT_PLAN_2_NO_NAMED_CONTACTS[c.support_plan]
               data["review_hours"] = REVIEW_HOURS_PER_QUARTER[c.support_plan]
               data["support_hours"] = SUPPORT_HOURS_PER_QUARTER[c.support_plan]
               f_data = json.dumps(data)
           elif c.support_plan == 'Premium':
               data["named_contacts"] = SUPPORT_PLAN_2_NO_NAMED_CONTACTS[c.support_plan]
               data["review_hours"] = REVIEW_HOURS_PER_QUARTER[c.support_plan]
               data["support_hours"] = SUPPORT_HOURS_PER_QUARTER[c.support_plan]
               f_data = json.dumps(data)

           elif c.support_plan == 'Enterprise':
               data["named_contacts"] = SUPPORT_PLAN_2_NO_NAMED_CONTACTS[c.support_plan]
               data["review_hours"] = REVIEW_HOURS_PER_QUARTER[c.support_plan]
               data["support_hours"] = SUPPORT_HOURS_PER_QUARTER[c.support_plan]
               f_data = json.dumps(data)
           elif c.support_plan == 'Partner':
               data["named_contacts"] = SUPPORT_PLAN_2_NO_NAMED_CONTACTS[c.support_plan]
               data["review_hours"] = REVIEW_HOURS_PER_QUARTER[c.support_plan]
               data["support_hours"] = SUPPORT_HOURS_PER_QUARTER[c.support_plan]
               f_data = json.dumps(data)
           else:
                f_data = []
           c.entitlements= f_data
           c.save()

        print "successfully updated"
