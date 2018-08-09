from django.contrib import admin
from .models import NotficationContact, TicketUnsubscriber


@admin.register(NotficationContact)
class NotficationContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'number', 'priority', 'enabled'
    )


@admin.register(TicketUnsubscriber)
class TicketUnsubscriberAdmin(admin.ModelAdmin):
    pass
