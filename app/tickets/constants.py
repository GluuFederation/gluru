from django.utils.translation import ugettext_lazy as _

TICKET_STATUS = (
    ('', 'Select a Status'),
    ('new', _('New')),
    ('assigned', _('Assigned')),
    ('inprogress', _('In Progress')),
    ('pending', _('Pending Input')),
    ('closed', _('Closed')),
)

TICKET_STATUS_CREATE = (
    ('new', _('New')),
    ('assigned', _('Assigned')),
    ('inprogress', _('In Progress')),
    ('pending', _('Pending Input')),
)

TICKET_STATUS_FILTER = (
    ('new', _('New')),
    ('assigned', _('Assigned')),
    ('inprogress', _('In Progress')),
    ('pending', _('Pending Input'))
)

TICKET_PRIVACY = (
    (False, _('Public')),
    (True, _('Private')),
)


ISSUE_TYPE_CREATE = (
    ('', _('Please specify the kind of issue you have encountered')),
    ('outage', _('Production Outage')),
    ('impaired', _('Production Impaired')),
    ('pre_production', _('Pre-Production Issue')),
    ('minor', _('Minor Issue')),
    ('new_development', _('New Development Issue'))
)

ISSUE_TYPE = (
    ('outage', _('Production Outage')),
    ('impaired', _('Production Impaired')),
    ('pre_production', _('Pre-Production Issue')),
    ('minor', _('Minor Issue')),
    ('new_development', _('New Development Issue'))
)

ISSUE_CATEGORY = (
    ('','Select an issue category'),
    ('installation','Installation'),
    ('outages','Outages'),
    ('single_sign_on','Single Sign-On'),
    ('authentication','Authentication'),
    ('authorization','Authorization'),
    ('access_management','Access Management'),
    ('upgrade','Upgrade'),
    ('maintenance','Maintenance'),
    ('identity_management','Identity Management'),
    ('customization','Customization'),
    ('feature_request','Feature Request'),
    ('log_out', 'Logout'),
    ('other', 'Other')
)

ISSUE_TYPE_FILTER = (
    ('outage', _('Production Outage')),
    ('impaired', _('Production Impaired')),
    ('pre_production', _('Pre-Production Issue')),
    ('minor', _('Minor Issue')),
    ('new_development', _('New Development Issue')),
    ('community', _('Community Tickets'))
)

ANSWER_PRIVACY = (
    ('inherit', _('Inherit')),
    ('public', _('Public')),
    ('private', _('Private')),
)

DATE_FILTER_TYPES = (
    ("eq", "Equals"),
    ("not_eq", "Not On"),
    ("gt", "After"),
    ("lt", "Before"),
    ("last_7_days", "Last 7 Days"),
    ("last_30_days", "Last 30 Days"),
    ("this_month", "This Month"),
    ("last_month", "Last Month"),
    ("this_year", "This Year"),
    ("last_year", "Last Year"),
)

# OS_VERSION = (
#     ('', 'Select Operating System'),
#     ('U1404', 'Ubuntu 14.04'),
#     ('CentOS65', 'CentOS 6.5'),
#     ('CentOS66', 'CentOS 6.6'),
#     ('CentOS67', 'CentOS 6.7'),
#     ('CentOS72', 'CentOS 7.2'),
#     ('Rhel65', 'RHEL 6.5'),
#     ('Rhel66', 'RHEL 6.6'),
#     ('Rhel67', 'RHEL 6.7'),
#     ('Rhel72', 'RHEL 7.2'),
#     ('Other', 'Other')
# )
OS_VERSION = (
    ('','Select Operating System'),
    ('Ubuntu', 'Ubuntu'),
    ('CentOS','CentOS'),
    ('Rhel' , 'RHEL'),
    ('Debian', 'Debian'),
    ('Other', 'Other')
)


PRODUCT_OS_VERSION = (
    ('','Select Operating System'),
    ('Ubuntu', 'Ubuntu'),
    ('CentOS','CentOS'),
    ('RHEL', 'RHEL'),
    ('Debian', 'Debian'),
    ('Android','Android'),
    ('iOS','iOS'),
    ('Both','Both')

)

GLUU_SERVER_VERSION = (
    ('', 'Select Gluu Server Version'),
    ('3.1.4', '3.1.4'),
    ('3.1.3', '3.1.3'),
    ('3.1.2', '3.1.2'),
    ('3.1.1', '3.1.1'),
    ('3.1.0', '3.1.0'),
    ('3.0.2', '3.0.2'),
    ('3.0.1', '3.0.1'),
    ('2.4.4', '2.4.4'),
    ('2.4.3', '2.4.3'),
    ('2.4.2', '2.4.2'),
    ('Other', 'Other'),
)

PRODUCT = (
    ('','Select a Product'),
    # ('GLUU','Gluu Server'),
    ('Oxd','OXD'),
    ('Super Gluu','Super Gluu'),
    ('Cluster','Cluster Manager'),
    ('Cred Manager','Cred Manager')
)

Product_Version = (
    ('','Select Product Version'),
    ('3.1.4','3.1.4'),
    ('3.1.3','3.1.3'),
    ('3.1.2','3.1.2'),
    ('3.1.1','3.1.1'),
    ('3.0.2','3.0.2'),
    ('3.0.1','3.0.1'),
    ('2.4.4.3','2.4.4.3'),
    ('2.4.4.2','2.4.4.2'),
    ('2.4.4','2.4.4'),
    ('2.4.3','2.4.3'),
    ('2.4.2','2.4.2'),
    ('1.0','1.0'),
    ('Alpha','Alpha'),
    ('Other','Other')
)

# OXD_Product_Version = (
#     ('','Select a Product Version'),
#     ('3.0.2','3.0.2'),
#     ('3.0.1','3.0.1')
# )
#
# Cluster_Gluu_Product_Version = (
#     ('','Select a Product Version'),
#     ('1','1.0')
# )

Gluu_Server_Issues = (
    ('','Select an Issue Category'),
    ('Installation','Installation'),
    ('Outage','Outage'),
    ('Sign-On','Single Sign-On'),
    ('Authentication','Authentication'),
    ('Authorization','Authorization'),
    ('Upgrade','Upgrade'),
    ('Maintenance','Maintenance'),
    ('Identity Management','Identity Management'),
    ('Customization','Customization'),
    ('Feature Request','Feature Request'),
    ('Other','Other')
)

OXD_Server_Issues =(
    ('','Select an Issue Category'),
    ('Installation','Installation'),
    ('Outage','Outage'),
    ('Authentication','Authentication'),
    ('Authorization','Authorization'),
    ('Upgrade','Upgrade'),
    ('Feature Request','Feature Request')
)

SUP_Gluu_Server_Issues =(
    ('','Select an Issue Category'),
    ('Installation','Installation'),
    ('Administration','Administration'),
    ('Enrollment','Enrollment'),
    ('Lost Device','Lost Device'),
    ('Feature Request','Feature Request')
)

TICKET_CATEGORY = (
    ('', 'Select a Category'),
    ('OUTAGE', 'Outages'),
    ('IDNTY', 'Identity Management'),
    ('SSO', 'Single Sign-On'),
    ('MFA', 'Authentication'),
    ('ACCESS', 'Access Management'),
    ('CUSTOM', 'Customization'),
    ('FEATURE', 'Feature Request'),
    ('INSTALLATION', 'Installation'),
    ('UPGRADE', 'Upgrade'),
    ('MAINTENANCE', 'Maintenance'),
    ('OTHER', 'Other'),
    ('LOGOUT', 'Log Out')
)
SMS_NUMBERS = (
    ('Your contact name','Your contact number'),

)
