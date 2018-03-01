from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from connectors.sugarcrm.crm_interface import get_support_plan_by_account
from profiles.models import Company
import json
class Command(BaseCommand):

    def handle(self, *args, **options):
        company = Company.objects.all()
        for c in company:
            plan = get_support_plan_by_account(c)
            if plan == 'None':
                c.support_plan = "Ex-Customer"
            elif plan == 'blank':
                c.support_plan = "Community"
            else:
                c.support_plan = plan
            c.save()

        print "successfully updated"
