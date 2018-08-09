from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from tickets import models


class AnswerInlineAdmin(admin.StackedInline):
    model = models.Answer
    extra = 0
    list_display = ('created_by', 'date_added', 'is_deleted')

    fieldsets = (
        (_('Base'), {'fields': (
            ('created_by', 'answer'),
            ('privacy', 'is_deleted'))}),
    )


class TicketsHistoryInlineAdmin(admin.StackedInline):
    model = models.TicketHistory
    extra = 0

    fieldsets = (
        (_('Base'), {'fields': (
            ('created_by', 'field_name'),
            ('before_value', 'after_value'))}),
    )


class TicketAlertsInlineAdmin(admin.StackedInline):

    model = models.TicketAlerts
    extra = 0
    fieldsets = (
        (_('Base'), {
            'fields': ('user',),
        }),
    )


class TicketAttachmentInlineAdmin(admin.TabularInline):
    model = models.TicketDocuments
    extra = 0
    readonly_fields = ['filename', 'created_by', 'date_added', 'is_deleted']
    fields = readonly_fields


class TicketAttachmentAdmin(admin.ModelAdmin):
    model = models.TicketDocuments
    readonly_fields = ['answer', 'ticket']
    list_display = ('id', 'file')
    ordering = ['-id']


class TicketsAdmin(admin.ModelAdmin):

    class Media:
        js = ('admin/js/custom.js',)

    def issue_type_display(self, obj):
        if obj.issue_type:
            return obj.issue_type
        return ''

    def activate_Ticket(self, obj):
        if obj.is_delete:
            return mark_safe('<a type="button" href="javascript:void(0);" class="activate_ticket" data-id="{0}" >Activate</a>'.format(obj.id))
        else:
            return ""

    model = models.Ticket

    list_display = (
        'id', 'title', 'status', 'issue_type_display', 'created_by', 'assigned_to',
        'modified_by', 'ticket_category', 'date_added', 'date_modified', 'is_deleted', 'activate_Ticket')

    search_fields = ('status', 'title', 'description')

    list_filter = ('ticket_category', 'issue_type', 'status', 'is_deleted', 'is_private')

    list_display_links = ['title', ]

    inlines = [AnswerInlineAdmin, TicketsHistoryInlineAdmin,
               TicketAlertsInlineAdmin, TicketAttachmentInlineAdmin]

    readonly_fields = ['date_added', 'date_modified', 'last_notification_sent']

    fieldsets = (
        (_('Base'), {
            'fields': (
                ('title', 'date_added'),
                ('description'),
                ('status', 'issue_type', 'ticket_category'),
                ('created_by', 'created_for', 'company_association'),
                ('date_modified', 'modified_by', 'last_notification_sent'),
                ('assigned_to'),
                ('link_url'),
            )
        }),
        (_('Status'), {
            'fields': ('is_deleted', 'is_private'),
        }),
        (_('Installation Info'), {
            'fields': (
                ('os_type', 'ram'),
                ('os_version'),
                ('gluu_server_version', 'gluu_server_version_comments')
            )
        }),
    )


class AnswerAdmin(admin.ModelAdmin):

    model = models.Answer

    inlines = [TicketAttachmentInlineAdmin, ]

    list_display = (
        'id', 'ticket', 'privacy', 'created_by', 'date_added',
        'date_modified', 'is_deleted'
    )

    search_fields = ('answer',)

    list_filter = ('privacy', 'is_deleted')

    list_display_links = ['ticket', ]

    fieldsets = (
        (_('Base'), {'fields': (
            ('answer'),
            ('ticket',),
            ('created_by', 'link_url'))}),
        ('Status', {
            'fields': (('is_deleted',),)
        }),
    )

    ordering = ['-id']

class TicketsHistoryAdmin(admin.ModelAdmin):
    model = models.TicketHistory

    list_display = ('ticket', 'created_by', 'field_name', 'date_added')
    search_fields = ('ticket', 'field_name')
    list_display_links = ['ticket', ]
    readonly_fields = ['date_added', ]
    fieldsets = (
        (_('Base'), {
            'fields': (
                ('ticket', 'created_by'),
                ('field_name', 'date_added'),
                ('before_value',),
                ('after_value',)
            )
        }),
    )


class TicketAlertsAdmin(admin.ModelAdmin):

    model = models.TicketAlerts

    list_display = ('ticket', 'user', 'date_added')
    search_fields = ('ticket', 'user')
    list_display_links = ['ticket']
    fieldsets = (
        (_('Base'), {
            'fields': ('ticket', 'user'),
        }),
    )


class TicketBlacklistAdmin(admin.ModelAdmin):

    model = models.TicketBlacklist

    list_display = ('ticket', 'user', 'date_added')
    search_fields = ('ticket', 'user')
    list_display_links = ['ticket']


admin.site.register(models.Ticket, TicketsAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.TicketHistory, TicketsHistoryAdmin)
admin.site.register(models.TicketAlerts, TicketAlertsAdmin)
admin.site.register(models.TicketBlacklist, TicketBlacklistAdmin)
admin.site.register(models.TicketDocuments, TicketAttachmentAdmin)
