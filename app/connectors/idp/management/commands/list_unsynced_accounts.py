from django.core.management.base import BaseCommand

from main.utils import log_idp

from profiles.models import UserProfile

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):

    def handle(self, *args, **options):

        count = 0
        for user in UserProfile.objects.filter(is_active=True, idp_uuid=''):
            count += 1
            log_idp('Unsynced account: {}, {}'.format(user.email, user.get_full_name()))

        log_idp('Total: {}'.format(count))
