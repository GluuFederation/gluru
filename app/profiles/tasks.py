from __future__ import absolute_import

from connectors.idp import idp_interface
from profiles import utils
from profiles.models import Activation, UserProfile
from main.celery import celery_app, CaptureFailure

@celery_app.task(base=CaptureFailure)
def send_activation_email(user_id):
    user = UserProfile.objects.get(id=user_id)
    idp_uuid = idp_interface.create_user(user)
    if 'user_exist' in idp_uuid:
        if idp_uuid.get('user_exist'):
            user.is_active = True
            user.idp_uuid = idp_uuid.get('uuid')
            user.save()
            utils.send_duplicate_account_notification(user)
    else:
        user.idp_uuid = idp_uuid
        activation_key = utils.generate_activation_key(user.email)
        activation = Activation(activation_key=activation_key, user=user)
        activation.save()
        utils.send_activation_email(user, activation_key)
        user.save()


@celery_app.task(base=CaptureFailure)
def confirm_registration(user_id, password):
    user = UserProfile.objects.get(id=user_id)
    user_idp = idp_interface.update_user(
    user=user, password=password)

    if user.is_basic:
        # TODO: move to asynchronous backend task
        utils.notify_company_admin(user)
    utils.send_new_user_notification(user)
    utils.send_activate_account_notification(user)
    user.username = user_idp.get('userName')
    user.save()
