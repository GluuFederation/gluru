from django.db import models
from django.utils.translation import ugettext as _
from tickets import constants


class Ticket(models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_('Title')
    )

    description = models.TextField(
        blank=False,
        null=False,
        verbose_name=_('Description')
    )

    category = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=constants.ISSUE_CATEGORY,
        verbose_name=_('Category')
    )

    created_by = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name=_('Created by')
    )

    created_for = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Created for')
    )

    company = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Company Association')
    )

    modified_by = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Last modified by')
    )

    assigned_to = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Assigned to')
    )

    status = models.CharField(
        max_length=100,
        choices=constants.TICKET_STATUS,
        blank=False,
        default='new',
        verbose_name=_('Status')
    )

    issue_type = models.CharField(
        max_length=20,
        choices=constants.ISSUE_TYPE_CREATE,
        blank=True,
        default='',
        verbose_name=_('Issue type')
    )

    answers_no = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_('Answers number')
    )

    link_url = models.URLField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Link URL')
    )

    send_copy = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Send copy to')
    )

    is_private = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Private')
    )

    is_deleted = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Deleted')
    )

    server_version = models.CharField(
        max_length=10,
        default='N/A',
        verbose_name=_('Gluu Server Version')
    )

    server_version_comments = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_('Gluu Server Version Comments')

    )

    os_version = models.CharField(
        choices=constants.OS_VERSION,
        max_length=8,
        blank=True,
        null=True,
        verbose_name=_('Which OS are you using?')
    )

    os_version_name = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('OS Version')
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Added')
    )

    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modified')
    )

    os_type = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Is it 64-bit hardware?')
    )

    ram = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Does the server have at least 4GB RAM?')
    )

    visits = models.IntegerField(
        blank=False,
        default=0,
        verbose_name=_('Ticket visits')
    )

    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('Meta keywords')
    )

    set_default_gluu = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Default Gluu'),
    )

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ['-date_added']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
