from django.db import models
from django.utils.translation import ugettext as _

from profiles.models import UserProfile


class CrmAccount(models.Model):

    profile = models.OneToOneField(
        UserProfile,
        related_name='sugar_crm'
    )

    sugarcrm_id = models.CharField(
        max_length=50,
        verbose_name=_('Unique identifier in SuiteCRM')
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )
