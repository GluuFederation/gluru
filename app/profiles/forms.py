from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import datetime
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div

from profiles.models import UserProfile, Company
from tickets import constants
from profiles.utils import oxd_cfg_file_data
from connectors.sugarcrm.crm_interface import get_partners
from connectors.idp.idp_interface import email_exists


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Email Address'}
        ),
        help_text=(
            '<p>If you are associated with a Gluu customer or partner organization, please use your organization specific email address.</p>'
        ),

    )

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        ),
    )

    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password'}
        )
    )

    first_name = forms.CharField(
        max_length=30,
        label=_('First Name'),
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name'}
        ),
        validators=[validators.MinLengthValidator(2)]
    )

    last_name = forms.CharField(
        max_length=30,
        label=_('Last Name'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name'}
        ),
        validators=[validators.MinLengthValidator(2)]
    )

    job_title = forms.CharField(
        max_length=100,
        label=_('Job Title'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Job Title'}
        ),
        validators=[validators.MinLengthValidator(2)]
    )

    mobile_number = forms.CharField(
        max_length=100,
        label=_('Mobile Phone Number'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Mobile Phone Number'}
        ),
        validators=[validators.MinLengthValidator(2)]
    )

    company = forms.CharField(
        max_length=100,
        label=_('Company'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Company'}
        ),
        validators=[validators.MinLengthValidator(2)]
    )

    class Meta:
        fields = ('email', 'first_name', 'last_name', 'job_title',
                  'mobile_number', 'company', 'timezone')
        model = UserProfile
        error_css_class = 'error_form'

    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Div(
                'first_name', 'last_name', 'email', 'company', 'job_title',
                'mobile_number', 'password1', 'password2', 'timezone'),
            FormActions(Submit('save', 'Submit')),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_exists(email):
            raise forms.ValidationError('A Gluu account with this email already exists.')
        return email

    def clean_password1(self):

        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')


class NamedRegistrationForm(RegistrationForm):

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    company = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):

        email = kwargs.pop('email', False)
        company = kwargs.pop('company', False)

        super(NamedRegistrationForm, self).__init__(*args, **kwargs)

        if email:
            self.fields['email'].initial = email
        if company:
            self.fields['company'].initial = company


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    company = forms.CharField()

    first_name = forms.CharField(
        max_length=100,
        required=True,
        label=_('First Name'),
        validators=[validators.MinLengthValidator(2)]
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        label=_('Last Name'),
        validators=[validators.MinLengthValidator(2)]
    )

    job_title = forms.CharField(
        max_length=100,
        required=True,
        label=_('Job Title'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Job Title'}),
        validators=[validators.MinLengthValidator(2)]
    )

    mobile_number = forms.CharField(
        max_length=100,
        required=True,
        label=_('Mobile Phone Number'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Mobile Phone Number'}),
        validators=[validators.MinLengthValidator(2)]
    )
    receive_all_notifications = forms.BooleanField(
        label='Subscribe to notifications for tickets created by your colleagues',
        required=False
    )

    class Meta:
        fields = ('email', 'first_name', 'last_name',
                  'job_title', 'mobile_number', 'company',
                  'timezone', 'receive_all_notifications')
        model = UserProfile
        error_css_class = 'error_form'

    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance.company:

            self.fields['company'] = forms.CharField(
                widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Div(
                'email', 'first_name', 'last_name', 'company',
                'job_title', 'mobile_number', 'timezone',
                'receive_all_notifications'
            ),
            FormActions(Submit('save', 'Save')),
        )


class InvitationForm(forms.Form):

    email = forms.EmailField(
        max_length=100,
        label=_('Invite via email'),
        widget=forms.TextInput(
            attrs={'placeholder': 'Email Address'})
    )

    class Meta:
        error_css_class = 'error_form'

    def __init__(self, *args, **kwargs):

        super(InvitationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Div('email',),
            FormActions(Submit('save', 'Submit')),
        )


class PartnerForm(forms.Form):

    partners = get_partners()

    # partner = forms.ModelChoiceField(
    partner = forms.CharField(
        # queryset=Company.objects.filter(name__in=partners),
        label=_('Partner Company'),
        # empty_label=_('Choose a Company')
    )

    class Meta:
        error_css_class = 'error_form'

    def __init__(self, *args, **kwargs):

        super(PartnerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Div('partner',),
            FormActions(Submit('save', 'Submit')),
        )

    def clean_partner(self):

        partner_company = self.cleaned_data.get('partner')

        try:
            Company.objects.get(name=partner_company)
            return partner_company

        except ObjectDoesNotExist:

            raise forms.ValidationError('There is no company with that name')

class OxdConfigurationForm(forms.Form):

    oxd_host = forms.CharField(
        max_length=100,
        label=_('Oxd Host'),
        required=True,

    )
    oxd_port = forms.IntegerField(
        label=_('Oxd Port'),
        required=True,
    )
    oxd_id = forms.CharField(
        max_length=150,
        label=_('Oxd ID'),
        required=True,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    client_op_host = forms.CharField(
        max_length=150,
        label=_('OP Host'),
        required=True,
    )
    client_authorization_redirect_uri= forms.CharField(
        max_length=200,
        label=_('Authorization Redirect Uri'),
        required=True,
    )
    client_post_logout_redirect_uri=forms.CharField(
        max_length=200,
        label=_('Post Logout Redirect Uri'),
        required=True,
    )
    client_scope = forms.CharField(
        max_length=200,
        label=_('Scope'),
        required=True,
    )
    client_id=forms.CharField(
        max_length=300,
        label=_('Client ID'),
        required=True,
    )
    client_secret=forms.CharField(
        max_length=300,
        label=_('Client Secret'),
        required=True,
    )
    client_grant_types=forms.CharField(
        max_length=300,
        label=_('Grant Types'),
        required=True,
    )
    client_id_issued_at=forms.CharField(
        max_length=300,
        label=_('Client ID Issued At'),
        required=True,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )

    class Meta:
        error_css_class = 'error_form'

    def __init__(self, *args, **kwargs):


        super(OxdConfigurationForm, self).__init__(*args, **kwargs)

        data = oxd_cfg_file_data()
        if data:
            self.fields['oxd_host'].initial = data[0] if data[0] != "N/A" else ""
            self.fields['oxd_port'].initial = data[1] if data[1] != "N/A" else ""
            self.fields['oxd_id'].initial = data[2] if data[2] != "N/A" else ""
            self.fields['client_op_host'].initial = data[3] if data[3] != "N/A" else ""
            self.fields['client_authorization_redirect_uri'].initial = data[4] if data[4] != "N/A" else ""
            self.fields['client_post_logout_redirect_uri'].initial = data[5] if data[5] != "N/A" else ""
            self.fields['client_scope'].initial = data[6] if data[6] != "N/A" else ""
            self.fields['client_id'].initial = data[7] if data[7] != "N/A" else ""
            self.fields['client_secret'].initial = data[8] if data[8] != "N/A" else ""
            self.fields['client_grant_types'].initial = data[9] if data[9] != "N/A" else ""
            if data[10] == "0":
                self.fields['client_id_issued_at'].initial =  datetime.datetime.now()
            else:
                self.fields['client_id_issued_at'].initial = data[10] if data[10] != "N/A" else ""


        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal oxd_form'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Div('oxd_host','oxd_port','oxd_id','client_op_host', 'client_authorization_redirect_uri',
                'client_post_logout_redirect_uri', 'client_scope', 'client_id', 'client_secret',
                'client_grant_types','client_id_issued_at'),
            FormActions(Submit('save', 'Submit')),
        )
