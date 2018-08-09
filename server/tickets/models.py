from django.db import models
from django.utils.translation import ugettext as _
from tickets import constants


class Ticket(models.Model):

    title = models.CharField(
        max_length=255
    )

    body = models.TextField()

    category = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.ISSUE_CATEGORY,
        default='IN',
        verbose_name=_('Category')
    )

    created_by = models.CharField(
        max_length=constants.UUID_MAX_LENGTH
    )

    created_for = models.CharField(
        max_length=constants.UUID_MAX_LENGTH,
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=constants.UUID_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name=_('Company Association')
    )

    updated_by = models.CharField(
        max_length=constants.UUID_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name=_('Last Updated by')
    )

    assignee = models.CharField(
        max_length=constants.UUID_MAX_LENGTH,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.TICKET_STATUS,
        default='NW'
    )

    issue_type = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.ISSUE_TYPE,
        default=''
    )

    server_version = models.CharField(
        max_length=constants.VERSION_CHOICE_MAX_LENGTH,
        choices=constants.GLUU_SERVER_VERSION,
        default='',
        help_text=_('Gluu Server Version')
    )

    server_version_comments = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Gluu Server Version Comments')
    )

    os_version = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.OS_VERSION,
        default='',
        verbose_name=_('OS'),
        help_text=_('Which OS are you using?')
    )

    os_version_name = models.CharField(
        max_length=10,
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
        verbose_name=_('Link URL')
    )

    send_copy = models.CharField(
        max_length=255,
        blank=True,
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
        help_text=_('Is it 64-bit hardware?')
    )

    ram = models.BooleanField(
        blank=True,
        default=False,
        help_text=_('Does the server have at least 4GB RAM?')
    )

    visits = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_('Ticket visits')
    )

    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    set_default_gluu = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Default Gluu'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class TicketProduct(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='products',
    )

    product = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.PRODUCT,
        blank=True
    )

    version = models.CharField(
        max_length=constants.VERSION_CHOICE_MAX_LENGTH,
        choices=constants.Product_Version,
        blank=True,
        verbose_name=_('Product Version')
    )

    os_version = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.PRODUCT_OS_VERSION,
        blank=True,
        verbose_name=_('Product OS Version')

    )

    os_version_name = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('Product OS Version')
    )

    ios_version_name = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('iOS Version')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Answer(models.Model):

    body = models.TextField()

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    created_by = models.CharField(
        max_length=20,
        help_text=_('Answer added by user')
    )

    link_url = models.URLField(
        max_length=255,
        blank=True,
        verbose_name=_('Link URL')
    )

    privacy = models.CharField(
        max_length=constants.CHOICE_MAX_LENGTH,
        choices=constants.ANSWER_PRIVACY,
        blank=True
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
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.ticket.title

    class Meta:
        ordering = ['-created_at']
