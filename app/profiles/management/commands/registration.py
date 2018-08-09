from django.core.management.base import BaseCommand
import logging
from profiles.models import UserProfile, Activation, Invitation, Company, Partnership, Registration
from profiles import utils

from connectors.idp import idp_interface
import re

SHA1_RE = re.compile('^[a-f0-9]{40}$')

logger = logging.getLogger('django')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            users = Registration.objects.filter(status='initial')[:1]
            if users:
                for usr in users:
                    usr.status = 'processing'
                    usr.save()
                    user = UserProfile.objects.get(id=usr.user_id)
                    user.idp_uuid = idp_interface.create_user(user)
                    user.save()
                    activation_key = utils.generate_activation_key(user.email)
                    activation = Activation(user=user, activation_key=activation_key)
                    activation.save()
                    utils.send_activation_email(user, activation_key)
                    usr.status = 'pending'
                    usr.save()
                    print "Activation email sent at {0}".format(user.email)
            else:
                print "No record found"
        except Exception as e:
            print e
