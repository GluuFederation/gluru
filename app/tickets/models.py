import os
import base64
from os.path import join, basename
from django.conf import settings
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext as _
from profiles.models import Company
from tickets import constants
from main.utils import log_error
from django.core.exceptions import ObjectDoesNotExist
from connectors.sugarcrm.crm_interface import get_support_plan

class Category:
    name = ''
    slug = ''
    tickets_no = 0
    tickets = []

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)

    def __repr__(self):
        return '{}: {}'.format(self.name, self.tickets_no)


class TicketManager(models.Manager):

    def get_active(self, user=None):

        q = [models.Q(is_deleted=False)]

        if not user:

            q.append(models.Q(is_private=False))

        elif user is not None:

            if user.is_anonymous():

                q.append(models.Q(is_private=False))

            elif user.is_named:

                clients = Company.objects.filter(
                    clients__is_deleted=False,
                    clients__partner=user.company_association
                )

                q.append(
                    models.Q(is_private=False) |
                    (models.Q(created_by=user) & models.Q(created_for=None)) |
                    models.Q(created_for=user) |
                    models.Q(company_association=user.company_association) |
                    models.Q(company_association__in=clients)
                )

            elif user.is_basic:

                q.append(
                    models.Q(is_private=False) |
                    models.Q(created_by=user)
                )

        return self.get_queryset().filter(*q)


class Ticket(models.Model):

    objects = TicketManager()

    WATCHING_FIELDS = [
        'assigned_to', 'status', 'is_deleted', 'issue_type',
        'title', 'description', 'created_for'
    ]

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

    ticket_category = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=constants.TICKET_CATEGORY,
        verbose_name=_('Category')
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        related_name='ticket_created_by',
        verbose_name=_('Created by')
    )

    created_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='ticket_created_for',
        verbose_name=_('On behalf of')
    )

    company_association = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        default=None,
        related_name='tickets'
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='ticket_modified_by',
        verbose_name=_('Last modified by')
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='ticket_assigned_to',
        verbose_name=_('Assigned to')
    )

    status = models.CharField(
        max_length=100,
        choices=constants.TICKET_STATUS,
        default='new',
        blank=False,
        verbose_name=_('Status')
    )

    issue_type = models.CharField(
        max_length=255,
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

    link_url = models.CharField(
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
    os_name = models.CharField(
        max_length=255,
        default='N/A',
        verbose_name=_('os_name')
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Added')
    )

    date_modified = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Modified')
    )

    last_notification_sent = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Last notification was sent')
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

    set_default_gluu = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Set Default Gluu')
    )

    gluu_server_version = models.CharField(
        max_length=255,
        default='N/A',
        verbose_name=_('Gluu Server Version')
    )

    gluu_server_version_comments = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name=_('Gluu Server Version')
    )

    visits = models.IntegerField(
        default=0,
        verbose_name=_('Ticket visits')
    )
    meta_keywords = models.CharField(

        max_length =500,
        blank =True,
        null = True,
        verbose_name = _('Meta keywords')
    )

    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):

        if kwargs.get('user', None):
            self.modified_by = kwargs['user']
            self.date_modified = timezone.now()

        super(Ticket, self).save()

        if kwargs.get('user', None):
            self.make_history(kwargs['user'])

    @property
    def last_updated_at(self):
        if self.date_modified > self.last_notification_sent:
            return self.date_modified
        return self.last_notification_sent

    @property
    def _dict(self):
        d = {}

        for field in self._meta.fields:
            if field.name in self.WATCHING_FIELDS:
                attr = field.name
                value = getattr(self, attr)
                if value is not None and isinstance(field, ForeignKey):
                    value = value.__unicode__()
                d[attr] = value
        return d

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    def make_history(self, user):
        fileds_diffs = self.diff

        for k, v in fileds_diffs.items():

            self.ticket_history.create(
                created_by=user,
                field_name=k,
                before_value=v[0],
                after_value=v[1]
            )

    @property
    def assigned_first_time(self):
        return self.assigned_to and self.__initial['assigned_to'] is None

    @property
    def is_delete(self):
        if self.is_deleted:
            return True
        else:
            return False
    @property
    def changed_fields(self):
        return self.diff.keys()

    @property
    def owned_by(self):

        if self.created_for:
            return self.created_for

        return self.created_by

    @property
    def priority(self):
        if self.issue_type:
            return self.issue_type
        else:
            return 'community'

    @property
    def privacy(self):
        if self.is_private:
            return 'private'
        return 'public'

    # TODO: Remove?
    @property
    def last_updated(self):
        last_answer = self.ticket_answers.last()

        if last_answer:
            return last_answer.created_by

        last_update = self.ticket_history.last()

        if last_update:

            try:
                return last_update.created_by
            except ObjectDoesNotExist:
                log_error('Last Update Created By not found: {}, {}'.format(last_update.id, self.id))

        return self.created_by

    def has_view_permission(self, user):

        if not self.is_private or user.is_admin:
            return True

        if user.is_anonymous():
            return False

        if self.owned_by == user:
            return True

        if (user.is_named and self.company_association == user.company_association):
            return True

        if user.is_partner_of(self.company_association):
            return True

        return False

    def has_edit_permission(self, user):

        if user.is_anonymous():
            return False

        if user.is_admin:
            return True

        if self.owned_by == user:
            return True

        if (user.is_named and self.company_association == user.company_association):
            return True

        if user.is_partner_of(self.company_association):
            return True

        return False

    def has_delete_permission(self, user):

        return self.has_edit_permission(user)

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

class TicketProduct(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        related_name='product_ticket_id',
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

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Added'),
        help_text=_('Added date')
    )

    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modified'),
        help_text=_('Modified date')
    )


class Answer(models.Model):

    answer = models.TextField(
        blank=False,
        null=False,
        verbose_name=_('Answer')
    )

    ticket = models.ForeignKey(
        Ticket,
        blank=False,
        null=False,
        related_name='ticket_answers',
        verbose_name=_('Ticket'),
        help_text=_('Ticket')
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        related_name='answer_created_by',
        verbose_name=_('Created by'),
        help_text=_('Answer added by user')
    )

    link_url = models.CharField(
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

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Added'),
        help_text=_('Added date')
    )

    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modified'),
        help_text=_('Modified date')
    )


    def __unicode__(self):
        try:
            return self.ticket.title
        except ObjectDoesNotExist:
            log_error('Answer without a ticket: {}'.format(self.id))
            return '{}'.format(self.id)

    @property
    def documents(self):
        return self.answer_documents.filter(is_deleted=False)

    @property
    def filename(self):
        return basename(self.attachment.name)

    @property
    def is_private(self):
        if self.privacy == 'inherit':
            return self.ticket.is_private
        if self.privacy == 'public':
            return False
        return True

    def support_plan(self):
        plan = get_support_plan(self.created_by)
        support_level = 'Community'
        if plan:
            if plan['support_plan'] == 'blank':
                support_level = "Community"
            else:
                support_level = plan['support_plan']
        return support_level

    class Meta:
        ordering = ['date_added']
        verbose_name = 'answer'
        verbose_name_plural = 'answers'


class TicketNotification(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        related_name='ticket',
        blank=False,
        null=False
    )

    is_txt_sent = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    is_call_sent = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    is_try = models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

class TicketHistory(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        related_name='ticket_history',
        blank=False,
        null=False
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ticket_history_by',
        blank=False,
        null=False
    )

    field_name = models.CharField(
        max_length=100,
        blank=True
    )

    before_value = models.TextField(
        blank=True,
        null=True
    )

    after_value = models.TextField(
        blank=True,
        null=True
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['date_added']
        verbose_name = 'ticket history'
        verbose_name_plural = 'tickets history'


class TicketAlerts(models.Model):

    ticket = models.ForeignKey(
        'Ticket',
        related_name='ticket_alerts'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_alerts',
        blank=False,
        null=False
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        unique_together = ('ticket', 'user')
        ordering = ['-date_added']
        verbose_name = 'alert'
        verbose_name_plural = 'alerts'


class TicketBlacklist(models.Model):

    ticket = models.ForeignKey(
        'Ticket',
        related_name='blacklist',
        null=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        unique_together = ('ticket', 'user')
        ordering = ['-date_added']


def ticket_file_path(instance, filename):

    if hasattr(instance.ticket, 'id'):

        head , tail = os.path.split(filename)
        if instance.ticket.is_private:
            return join('protected', 'ticket', str(instance.ticket.id), tail)

        return join('ticket', str(instance.ticket.id), tail)
    else:

        if instance.answer.is_private:
            return join('protected', 'answer', str(instance.answer.ticket.id), filename)

        return join('answer', str(instance.answer.ticket.id), filename)


class TicketDocuments(models.Model):

    file = models.FileField(
        max_length=255,
        blank=True,
        upload_to=ticket_file_path
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='document_added_by',
        blank=False,
        null=False
    )

    ticket = models.ForeignKey(
        'Ticket',
        related_name='ticket_documents',
        blank=True,
        null=True
    )

    answer = models.ForeignKey(
        'Answer',
        related_name='answer_documents',
        blank=True,
        null=True
    )

    is_deleted = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Deleted'),
        help_text=_('The document has been deleted?')
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    file_src = models.TextField(
        blank = True,
        verbose_name= _('File Source')
    )

    @property
    def filename(self):
        return basename(self.file.name)

    class Meta:
        ordering = ['date_added']
        verbose_name = 'ticket document'
        verbose_name_plural = 'ticket documents'
