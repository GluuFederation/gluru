from django.utils.translation import ugettext_lazy as _

CHOICE_MAX_LENGTH = 2
VERSION_CHOICE_MAX_LENGTH = 10
UUID_MAX_LENGTH = 20
TICKET_STATUS = (
    ('', 'Select a Status'),
    ('NW', _('New')),
    ('AS', _('Assigned')),
    ('IP', _('In Progress')),
    ('PI', _('Pending Input')),
    ('CL', _('Closed')),
)

ISSUE_TYPE = (
    ('', _('Please specify the kind of issue you have encountered')),
    ('PO', _('Production Outage')),
    ('PI', _('Production Impaired')),
    ('PP', _('Pre-Production Issue')),
    ('MI', _('Minor Issue')),
    ('NI', _('New Development Issue'))
)

ISSUE_CATEGORY = (
    ('', 'Select a category'),
    ('IN', 'Installation'),
    ('OA', 'Outages'),
    ('SO', 'Single Sign-On'),
    ('AU', 'Authentication'),
    ('AZ', 'Authorization'),
    ('AM', 'Access Management'),
    ('UG', 'Upgrade'),
    ('MT', 'Maintenance'),
    ('IM', 'Identity Management'),
    ('CZ', 'Customization'),
    ('FR', 'Feature Request'),
    ('LO', 'Logout'),
    ('OH', 'Other')
)

ANSWER_PRIVACY = (
    ('', _('---------')),
    ('IH', _('Inherit')),
    ('PU', _('Public')),
    ('PR', _('Private')),
)

OS_VERSION = (
    ('', 'Select Operating System'),
    ('UT', 'Ubuntu'),
    ('CO', 'CentOS'),
    ('RH', 'RHEL'),
    ('DB', 'Debian')
)


PRODUCT_OS_VERSION = (
    ('', 'Select Operating System'),
    ('UT', 'Ubuntu'),
    ('CO', 'CentOS'),
    ('RH', 'RHEL'),
    ('DB', 'Debian'),
    ('AD', 'Android'),
    ('IO', 'iOS'),
    ('BO', 'Both')
)

PRODUCT = (
    ('', 'Select a Product'),
    ('OD', 'OXD'),
    ('SG', 'Super Gluu'),
    ('CM', 'Cluster Manager')
)

GLUU_SERVER_VERSION = (
    ('', 'Select Gluu Server Version'),
    ('3.1.2', 'Gluu Server 3.1.2'),
    ('3.1.1', 'Gluu Server 3.1.1'),
    ('3.1.0', 'Gluu Server 3.1.0'),
    ('3.0.2', 'Gluu Server 3.0.2'),
    ('3.0.1', 'Gluu Server 3.0.1'),
    ('2.4.4.3', 'Gluu Server 2.4.4.3'),
    ('2.4.4.2', 'Gluu Server 2.4.4.2'),
    ('2.4.4', 'Gluu Server 2.4.4'),
    ('2.4.3', 'Gluu Server 2.4.3'),
    ('2.4.2', 'Gluu Server 2.4.2'),
    ('Other', 'Other')
)

Product_Version = (
    ('', 'Select Product Version'),
    ('3.1.1', '3.1.1'),
    ('3.0.2', '3.0.2'),
    ('3.0.1', '3.0.1'),
    ('2.4.4.3', '2.4.4.3'),
    ('2.4.4.2', '2.4.4.2'),
    ('2.4.4', '2.4.4'),
    ('2.4.3', '2.4.3'),
    ('2.4.2', '2.4.2'),
    ('1.0', '1.0'),
    ('Alpha', 'Alpha'),
    ('Other', 'Other')
)

SMS_NUMBERS = (
    ('Your contact name', 'Your contact number'),
)
