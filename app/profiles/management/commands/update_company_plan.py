from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from connectors.sugarcrm.crm_interface import get_support_plan_by_account
from profiles.constants import SUPPORT_PLAN_2_NO_NAMED_CONTACTS,REVIEW_HOURS_PER_QUARTER,SUPPORT_HOURS_PER_QUARTER
from profiles.models import Company
import json
class Command(BaseCommand):

    def handle(self, *args, **options):
        company = Company.objects.all()
        for c in company:
            plan = get_support_plan_by_account(c, company_type=True)
            is_all_none = lambda L: not len(filter(lambda e: not plan is None, L))
            if is_all_none([None, None, None]):
                c.support_plan = "ex_customer"
                c.type = "ex_customer"
                c.managed_service = 0
            else:
                if plan[3] is not None:
                    c.managed_service = plan[3]
                if plan[0] and plan[1]:
                    if plan[0] == 'blank' and plan[1] == "ex_customer":
                        c.support_plan = "ex_customer"
                        c.type = "ex_customer"
                    else:
                        if plan[0] == 'blank':
                            c.support_plan = plan[1]
                        else:
                            c.support_plan = plan[0]
                        c.type = plan[1]
                elif plan[0] == 'blank' and plan[1]:
                    c.support_plan = plan[1]
                    c.type = plan[1]
                elif plan[0] == 'blank' and plan[1] is None:
                    c.support_plan = ""
                    c.type = "ex_customer"
            c.save()
        print "successfully updated"
