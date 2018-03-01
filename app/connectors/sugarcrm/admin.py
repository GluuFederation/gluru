from django.contrib import admin
from connectors.sugarcrm.models import CrmAccount


class CrmAccountsAdmin(admin.ModelAdmin):
    model = CrmAccount
    list_display = ('profile', 'sugarcrm_id', 'last_updated')

admin.site.register(CrmAccount, CrmAccountsAdmin)
