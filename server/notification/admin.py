from django.contrib import admin
from .models import NotficationContact, TicketNotification


@admin.register(NotficationContact)
class NotficationContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'number', 'priority', 'enabled'
    )


@admin.register(TicketNotification)
class TicketNotificationAdmin(admin.ModelAdmin):
    pass
