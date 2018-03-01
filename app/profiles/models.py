import pytz
import json
import datetime
import time
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)

from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from profiles import constants


CONT_TYPE = (
    ('', '---------'),
    (constants.STAFF, 'Staff'),
    (constants.MANAGER, 'Manager'),
    (constants.ADMIN, 'Admin'),
    (constants.NAMED, 'Named'),
    (constants.USER, 'User'),
)


class Company(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )

    support_plan = models.CharField(
        _('support plan'),
        max_length=100,
        blank=True
    )
    entitlements = models.CharField(
        _('entitlements'),
        max_length=500,
        blank=True
    )
    class Meta:
        verbose_name_plural = 'companies'
        ordering = ['name']

    def __str__(self):
        return self.name

class Entitlements(models.Model):


    plan =  models.CharField(
        _('plan'),
        max_length=100
    )

    entitlements = models.CharField(
        _('entitlements'),
        max_length=500,
        blank=True
    )
    created_at = models.DateField(
        _('created_at'),
        auto_now_add=True,
    )
    updated_at = models.DateField(
        _('updated_at'),
        auto_now_add=True,
    )


    class Meta:
        verbose_name_plural = 'entitlements'
        ordering = ['plan']

    def __str__(self):
        return self.plan


    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Entitlements, self).save()
        company =  Company.objects.filter(support_plan=self.plan)
        from connectors.sugarcrm.crm_interface import get_support_plan_by_account
        for cmp in company:
                company_renewal_date = str(get_support_plan_by_account(cmp,1))
                updated_at = str(self.updated_at).split(" ")
                if company_renewal_date < updated_at[0]:
                    cmp.entitlements = self.entitlements
                    cmp.save()


class Meeting(models.Model):

    date = models.DateField()

    duration_in_minutes = models.IntegerField(
        default=30
    )

    company = models.ForeignKey(
        Company,
        related_name='meetings'
    )

    meeting_type = models.CharField(
        max_length=30,
        choices=constants.MEETING_TYPE
    )


def create_or_get_company(name, support_plan):

    try:

        return Company.objects.get(name=name)

    except ObjectDoesNotExist:

        company = Company(name=name)
        if support_plan:
           company.support_plan = support_plan
           data = {}
           entitlements= Entitlements.objects.get(plan=support_plan)
           entitlement_data= json.loads(entitlements.entitlements)
           data["named_contacts"] = entitlement_data["named_contacts"]
           data["review_hours"] = entitlement_data["review_hours"]
           data["support_hours"] = entitlement_data["support_hours"]
           f_data = json.dumps(data)
           company.entitlements= f_data
        company.save()
        return company


class UserProfileManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()

        if not email:
            raise ValueError(_('You need to provide an email address'))

        email = self.normalize_email(email)

        is_active = extra_fields.pop('is_active', True)

        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user
        """
        is_staff = extra_fields.pop('is_staff', False)
        return self._create_user(username, email, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        username = email.split('@')[0]
        return self._create_user(username, email, password, True, True, **extra_fields)


class AbstractUserProfile(AbstractBaseUser, PermissionsMixin):

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = models.CharField(
        _('username'),
        max_length=100,
        blank=True,
        default=''
    )

    first_name = models.CharField(
        _('first name'),
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        _('last name'),
        max_length=100,
        blank=True
    )

    job_title = models.CharField(
        _('job title'),
        max_length=100,
        blank=True,
    )

    mobile_number = models.CharField(
        _('mobile number'),
        max_length=100,
        blank=True,
    )

    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last change'),
        help_text=_('Last change'),
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='Company info added by user upon registration'
    )

    company_association = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        default=None,
        related_name='named_users'
    )

    crm_type = models.CharField(
        max_length=30,
        choices=CONT_TYPE,
        default='user'
    )

    is_company_admin = models.BooleanField(
        blank=True,
        default=False
    )

    idp_uuid = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    crm_uuid = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    timezone = models.CharField(
        max_length=50,
        choices=[(x, x) for x in pytz.common_timezones],
        blank=False,
        default='US/Central'
    )

    receive_all_notifications = models.BooleanField(
        blank=True,
        default=False,
        help_text='Subscribe to notifications for tickets created by your colleagues'
    )

    def __unicode__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        abstract = True

    def get_company(self):

        if self.company_association:
            return self.company_association.name

        return self.company

    @property
    def get_is_company_admin(self):
        if self.is_company_admin:
            return True
        return False

    @property
    def get_type(self):
        if self.crm_type in ['manager', 'admin', 'staff']:
            return 'staff'
        return self.crm_type

    @property
    def is_admin(self):
        if self.crm_type in ['staff', 'admin', 'manager']:
            return True
        return False



    @property
    def is_named(self):
        if self.crm_type == 'named':
            return True
        return False

    @property
    def staff(self):
        if self.is_staff:
            return True
        return False

    @property
    def is_basic(self):
        if self.crm_type == 'user':
            return True
        return False

    @property
    def profile_incomplete(self):

        if not self.is_basic:
            return False

        fields = ['first_name', 'last_name', 'company',
                  'job_title', 'mobile_number']

        for field in fields:
            if not getattr(self, field):
                return True

        return False

    def is_partner_of(self, client):

        try:
            Partnership.objects.get(
                client=client,
                partner=self.company_association,
                is_deleted=False
            )

            return True

        except ObjectDoesNotExist:

            return False

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name


class UserProfile(AbstractUserProfile):
    """
    Concrete class of AbstractUserProfile.
    Use this if you don't need to extend UserProfile.
    """
    class Meta(AbstractUserProfile.Meta):
        swappable = 'AUTH_USER_MODEL'


class Activation(models.Model):

    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='activation'
    )

    activation_key = models.CharField(
        _('activation key'),
        max_length=40
    )

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )

class Invitation(models.Model):

    email = models.EmailField(
        blank=False,
        null=False,
        unique=False
    )

    invited_by = models.ForeignKey(
        UserProfile,
        blank=False,
        null=False,
        unique=False,
        related_name='invites'
    )

    activation_key = models.CharField(
        _('activation key'),
        max_length=40
    )

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )


class Partnership(models.Model):

    client = models.ForeignKey(
        Company,
        related_name='clients',
        on_delete=models.CASCADE
    )

    partner = models.ForeignKey(
        Company,
        related_name='partners',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
