from django.contrib import admin
from .models import Ticket, Answer, TicketProduct, TicketHistory


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at')


@admin.register(TicketProduct)
class TicketProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ticket', 'privacy', 'created_by', 'created_at',
        'updated_at', 'is_deleted'
    )


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'ticket', 'changed_by', 'changed_field',
        'before_value', 'after_value'
    )
