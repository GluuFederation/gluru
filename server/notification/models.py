from django.db import models
from django.utils.translation import ugettext as _
from tickets.models import Ticket
from tickets.constants import UUID_MAX_LENGTH


class NotficationAvailableContact(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enabled=True)


class NotficationContact(models.Model):

    PRIORITY_HIGH = 'H'
    PRIORITY_LOW = 'L'
    PRIORITY = (
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_LOW, 'Low')
    )

    name = models.CharField(
        max_length=100,
        help_text=_('Contact name')
    )

    number = models.CharField(
        max_length=100,
        help_text=_('Contact Number')
    )

    priority = models.CharField(
        max_length=1,
        choices=PRIORITY,
        default=PRIORITY_HIGH,
        help_text=_('Priority')
    )

    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Is Enabled?')
    )

    objects = models.Manager()
    availables = NotficationAvailableContact()

    class Meta:
        ordering = ['priority']


class TicketNotificationSubscriberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_subscribed=True)


class TicketNotificationUnSubscriberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_subscribed=False)


class TicketNotification(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='blacklist',
    )

    user = models.CharField(
        max_length=UUID_MAX_LENGTH,
        help_text=_('User associated with this ticket notification')
    )

    is_subscribed = models.BooleanField(
        default=True,
        help_text=_('Indicate whether user subscribe to notification')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    objects = models.Manager()
    subscribers = TicketNotificationSubscriberManager()
    unsubscribers = TicketNotificationUnSubscriberManager()

    class Meta:
        unique_together = ('ticket', 'user')
        ordering = ['-created_at']
