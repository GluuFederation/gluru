from django.contrib import admin
from tickets.models import Ticket, Answer, TicketProduct


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
