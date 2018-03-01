from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles import models
from connectors.sugarcrm.crm_interface import get_support_plan_by_account

class UserProfileAdmin(UserAdmin):

    ordering = ('-id',)
    search_fields = ['email', 'company', 'first_name', 'last_name']
    model = models.UserProfile

    list_display = (
        'id', 'first_name', 'last_name', 'email',
        'crm_type', 'company_association', 'is_active',
        'is_company_admin', 'is_staff', 'last_login', 'date_joined', 
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': (
            'company', 'job_title', 'mobile_number', 'crm_type', 'timezone')}),
        ('Paying users', {'fields': (
            'company_association', 'is_company_admin',)}),
        ('Syncing', {'fields': ('idp_uuid', 'crm_uuid')}),
        ('Notifications', {'fields': ('receive_all_notifications',)}),
    )

admin.site.register(models.UserProfile, UserProfileAdmin)


class ActivationAdmin(admin.ModelAdmin):

    model = models.Activation

    list_display = ('id', 'user', 'activation_key', 'created')

admin.site.register(models.Activation, ActivationAdmin)


class InvitationAdmin(admin.ModelAdmin):

    model = models.Invitation

    list_display = ('id', 'email', 'invited_by', 'activation_key', 'created')

admin.site.register(models.Invitation, InvitationAdmin)


class UserInline(admin.TabularInline):

    model = models.UserProfile
    fields = ['email', 'first_name', 'last_name']
    readonly_fields = fields
    extra = 0

class MeetingInline(admin.TabularInline):

    model = models.Meeting
    fields = ['date', 'meeting_type', 'duration_in_minutes']
    extra = 1

class EntitlementsAdmin(admin.ModelAdmin):

    model= models.Entitlements

    list_display =('id', 'plan', 'entitlements','created_at','updated_at')

admin.site.register(models.Entitlements, EntitlementsAdmin)

class CompanyAdmin(admin.ModelAdmin):

    model = models.Company
    def support_plan(self, obj):
        plan = get_support_plan_by_account(obj.name)
        if plan == "blank":
            return "Community"
        elif not plan:
            return "Ex Customer"
        else:
            return plan

    readonly_fields=['support_plan']

    list_display = ('id', 'name', 'created', 'support_plan', 'entitlements')

    inlines = [UserInline, MeetingInline]

admin.site.register(models.Company, CompanyAdmin)


class PartnershipAdmin(admin.ModelAdmin):

    model = models.Partnership

    list_display = ('id', 'client', 'partner', 'created', 'is_deleted')

admin.site.register(models.Partnership, PartnershipAdmin)
