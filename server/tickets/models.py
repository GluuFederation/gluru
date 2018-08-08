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

    updated_by = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Last Updated by')
    )

    assignee = models.CharField(
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

    server_version = models.CharField(
        max_length=10,
        choices=constants.GLUU_SERVER_VERSION,
        blank=False,
        default='',
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

    answers_no = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_('Answers number')
    )

    link = models.URLField(
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

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class TicketProduct(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        related_name='products',
        blank=False,
        null=False
    )

    product = models.CharField(
        max_length=20,
        choices=constants.PRODUCT,
        blank=True,
        default='',
        verbose_name=_('Product')
    )


    product_version = models.CharField(
        max_length=20,
        choices=constants.Product_Version,
        blank=True,
        default='',
        verbose_name=_('Product Version')
    )

    product_os_version = models.CharField(
        max_length=20,
        choices=constants.PRODUCT_OS_VERSION,
        blank=True,
        default='',
        verbose_name=_('Product OS Version')

    )
    product_os_version_name = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Product OS Version')
    )

    ios_version_name = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('iOS Version')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created At'),
        help_text=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At'),
        help_text=_('Updated At')
    )


class Answer(models.Model):

    answer = models.TextField(
        blank=False,
        null=False,
        verbose_name=_('Answer')
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_answers',
        verbose_name=_('Ticket'),
        help_text=_('Ticket')
    )

    created_by = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name=_('Created by'),
        help_text=_('Answer added by user')
    )

    link_url = models.URLField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Link URL')
    )

    privacy = models.CharField(
        max_length=255,
        choices=constants.ANSWER_PRIVACY,
        default='inherit',
        blank=True,
        verbose_name=_('Privacy')
    )

    send_copy = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Send copy to')
    )

    is_deleted = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Deleted'),
        help_text=_('The answer is deleted?')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Added'),
        help_text=_('Added date')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modified'),
        help_text=_('Modified date')
    )

    def __str__(self):
        return self.ticket.title

    class Meta:
        ordering = ['created_at']
        verbose_name = 'answer'
        verbose_name_plural = 'answers'
