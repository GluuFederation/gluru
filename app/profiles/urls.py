from django.conf.urls import url

from profiles import views
from profiles import gluu_oxd

urlpatterns = [
    url(
        r'^logout/$',
        gluu_oxd.get_logout,
        name='logout'
    ),
    url(
        r'^dashboard/(?P<page_type>[A-Za-z\-_]+)/$',
        views.dashboard,
        name='dashboard'
    ),

    url(
      	r'^reset_oxd_values/$',
        views.reset_oxd_values,
        name='reset_oxd_values'
    ),
    url(
        r'^register/$',
        views.register,
        name='register'
    ),
    url(
        r'^registered/(?P<name>\w+)/$',
        views.register,
        name='registered'
    ),
    url(
        r'^register/(?P<activation_key>\w+)/$',
        views.register_named,
        name='register-named'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        views.activate,
        name='activate'
    ),
    url(
        r'^dashboard/my-profile/$',
        views.my_profile,
        name='my-profile'
    ),
    url(
        r'^company-users/$',
        views.add_company_user,
        name='company-users'
    ),
    url(
        r'^company-users/revoke/(?P<user_id>[0-9]+)/$',
        views.revoke_access,
        name='revoke-access'
    ),
    url(
        r'^company-users/resend-invite/$',
        views.resend_invite,
        name='resend-invite'
    ),
    url(
        r'^company-users/revoke-invite/$',
        views.revoke_invite,
        name='revoke-invite'
    ),
    url(
        r'^company-users/invite-admin/(?P<user_id>[0-9]+)/$',
        views.add_company_admin,
        name='add-company-admin'
    ),
    url(
        r'^company-users/remove-admin/(?P<user_id>[0-9]+)/$',
        views.remove_company_admin,
        name='remove-company-admin'
    ),
    url(
        r'inactive-user/$',
        views.inactive_user,
        name='incative-user'
    ),
    url(
        r'^company-partners/$',
        views.add_company_partner,
        name='company-partners'
    ),
    url(
        r'^company-partners/revoke/(?P<partnership_id>[0-9]+)/$',
        views.revoke_partner,
        name='revoke-partner'
    ),
    url(
        r'^company-booking/$',
        views.book_meeting,
        name='booking'
    ),
    url(
        r'^accept/(?P<activation_key>\w+)/$',
        views.accept_invite,
        name='accept-invite'
    ),
    url(
        r'view_users/(?P<page_type>[A-Za-z\-_]+)/$',
        views.view_users,
        name='view_users'
    ),
    url(
        r'authorize/$',
        gluu_oxd.authorize,
        name='authorize'
    ),

    url(
        r'callback/$',
        gluu_oxd.callback,
        name='calllback'
    ),
    url(
        r'setup_client/$',
        gluu_oxd.setup_client,
        name='setup_client'
    )
]