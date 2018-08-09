from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit, HTML, Layout, Field, Reset, Div)
from crispy_forms.bootstrap import (
    FormActions, PrependedText,
    FieldWithButtons, StrictButton)

from tickets import constants
from tickets.models import Ticket, Answer,TicketProduct
from tickets.utils import generate_ticket_link ,product_select_list,product_version_select_list,\
    product_os_version_select_list ,gluu_server_version_select_list,gluu_os_version_list,get_last_ticket_data

from profiles.models import UserProfile, Company
from profiles import constants as pc
from pagedown.widgets import AdminPagedownWidget


class UserTicketForm(forms.ModelForm):

    gluu_server_version = forms.ChoiceField(
        label=_('Gluu Server Version'),
        choices=constants.GLUU_SERVER_VERSION
    )
    gluu_server_version_comments = forms.CharField(
        label=_('Gluu Server Version'),
        required=False
    )
    product = forms.ChoiceField(
        label=_('Select Product'),
        choices=constants.PRODUCT,
        required=False
    )
    product_version= forms.ChoiceField(
        label=_('Version'),
        choices=constants.Product_Version,
        required=False
    )
    product_os_version = forms.ChoiceField(
        label=_('Operating System'),
        choices=constants.PRODUCT_OS_VERSION,
        required=False
    )
    product_os_version_name = forms.FloatField(
        label=_('OS Version'),
        required=False
    )
    ios_version_name = forms.FloatField(
        label = _('iOS Version'),
        required=False
    )
    os_version = forms.ChoiceField(
        label=_('Operating System'),
        choices=constants.OS_VERSION
    )

    os_version_name = forms.FloatField(
        label=_('OS Version')
    )

    os_name = forms.CharField(
        label = _('Other Operating System'),
        required=False
    )

    ios_version_name = forms.FloatField(
        label = _('iOS Version'),
        required=False
    )

    set_default_gluu = forms.BooleanField(
        label=_('Set as Default'),
        required = False
    )


    description = forms.CharField(
        widget=forms.Textarea,
        help_text=(
            'This field supports <a target="_blank" href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet">markdown formatting.</a>'
        )
    )
    ticket_category = forms.ChoiceField(
        label=_('Choose a category'),
        choices=constants.TICKET_CATEGORY
    )

    classification_layout = Layout(
        Div(
            Div(
                Field('gluu_server_version', wrapper_class='col-md-4', css_class='gluu_server_version'),
                Field('gluu_server_version_comments', wrapper_class='col-md-3 hidden',  css_class='gluu_server_version_comments'),
                Field('os_version',wrapper_class='col-md-4 ', css_class="os_version "),
                Field('os_version_name',wrapper_class='col-md-4 os_version_icon', placeholder="Which OS are you using?", css_class="os_version_name "),
				Field('os_name', wrapper_class='col-md-4 hidden', placeholder='Which OS are you using?', css_class="os_name "),                
				css_class='gluu_layout_div'
            ),
            Div(
               HTML('<div class="col-md-6 add-product ">'),
               StrictButton('Add Product',css_class='add_product_btn '),
               HTML('</div>'),
               css_class= 'default_product_div'
        ),
            css_class='main_gluu_div'
        ),


    )

    product_layout= Layout(
         Div(
             Div(
                Field('product',wrapper_class='col-md-3 hidden' , css_class="product"),
                Field('product_version',wrapper_class='col-md-3 ', css_class="product_version "),
                Field('product_os_version',wrapper_class='col-md-3 ', css_class="product_os_version "),
                Field('product_os_version_name',wrapper_class='col-md-2  os_version_icon ', placeholder="os version", css_class="product_os_version_name"),
                Field('ios_version_name',wrapper_class='col-md-1 hidden os_version_icon', placeholder="ios version", css_class="ios_version_name"),
                HTML('<div class="col-md-1 remove"><a class="delete_product_row hidden" href="javascript:void(0);"></a><a class="delete_product_row mobile hidden" href="javascript:void(0);">Remove Product</a></div>'),
                css_class='product_layout_div layout_sec '

             ),


             css_class= 'main_product_div layout_sec hidden'
         ),


    )
    description_layout = Layout(
        Div(
            Field(
                'title',
                placeholder='Ticket title', wrapper_class='col-md-12'
            ),
        css_class= 'layout_sec'
        ),
        Div(
            Field(
                'description', wrapper_class='col-md-12',
                placeholder='Ticket description.. please include enough ' +
                'information for someone to reproduce your issue, ' +
                'including all relevant logs.',
                # data_uk_htmleditor='{mode:\'tab\',markdown:true}'
            ),
        css_class= 'layout_sec'
        )
    )

    category_layout = Layout(
        Div(
            Field('issue_type',wrapper_class='col-md-6'),
            Field('ticket_category',wrapper_class='col-md-6'),
        css_class= 'layout_sec'
        ),
    )

    additional_layout = Layout(
        Div(
            PrependedText(
                'send_copy',
                '<span class="glyphicon glyphicon-envelope"></span>',
                placeholder='Separate emails with commas'
            ),
            Field('is_private'),
            css_class= 'layout_sec'
        ),
        Div(
            PrependedText(
                'link_url',
                '<span class="glyphicon glyphicon-link"></span>',
                placeholder='URL to download/view ticket info'
            ),
            css_class= 'layout_sec'
        ),

    )

    button_layout = Div(
        FormActions(
            Submit('save', 'Submit'),
            HTML('<a class="btn btn-default" href="{% url \'home\'%}" id="cancelButton">Cancel</a>')
        ),
        css_class= 'layout_sec'
    )

    uploaded_products_layout = Layout()
    uploaded_classification_layout = Layout()

    class Meta:

        model = Ticket
        error_css_class = 'error_form'
        fields = ('product','product_version','product_os_version','product_os_version_name','ios_version_name','gluu_server_version','gluu_server_version_comments', 'os_version','os_version_name','os_name',
                  'title', 'description', 'ticket_category', 'link_url',
                  'send_copy')

    def __init__(self, user='null', *args, **kwargs):

        super(UserTicketForm, self).__init__(*args, **kwargs)
        self.uploaded_products_layout = Layout()
        self.uploaded_classification_layout = Layout()
        data = None
        if user:
            data = get_last_ticket_data(user)

        if data:
            self.fields['gluu_server_version'].initial = data[0] if data[0] != "N/A" else ""
            self.fields['os_version'].initial = data[1] if data[1] != None else ""
            self.fields['os_version_name'].initial = data[2] if data[2] != "" else 0
            self.fields['gluu_server_version_comments'].initial = data[3] if data[3] != "" else 0
            self.fields['os_name'].initial = data[4] if data[4] != "N/A" else ""

        self.fields['send_copy'].label = "CC Colleagues"
        self.fields['title'].label = "Subject"
        self.button_layout[0][0] = Submit('save', 'Submit')
        self.button_layout[0][1] = HTML(
            '<a class="btn btn-danger" href="{% url \'home\'%}" id="cancelButton">Cancel</a>')

        if self.instance.id:
            self.button_layout[0][0] = Submit('save', 'Save')
            self.button_layout[0][1] = HTML(
                '<a class="btn btn-danger" href="{}" id="cancelButton">Cancel</a>'.format(
                    generate_ticket_link(self.instance)))
            if self.instance.product_ticket_id.all():
                for ticket in self.instance.product_ticket_id.all():
                    if ticket.ios_version_name:
                        html= HTML('''
                            <div class="product_layout_div layout_sec"> <div id="div_id_product" class="form-group col-md-3 for-margin"> <label for="id_product" class="control-label  requiredField">
                                        Select Product<span class="star">*</span> </label> {} </div> <div id="div_id_product_version" class="form-group col-md-2 for-margin"> <label for="id_product_version" class="control-label  requiredField">
                                        Product Version<span class="star">*</span> </label> {} </div> <div id="div_id_product_os_version" class="form-group col-md-2 for-margin"> <label for="id_product_os_version" class="control-label  requiredField">
                                        Operating System<span class="star">*</span> </label> {} </div> <div id="div_id_product_os_version_name" style="width:128px;" class="form-group col-md-1 for-margin os_version_icon"> <label for="id_product_os_version_name" class="control-label  requiredField">
                                        Android Version<span class="star">*</span></label> <div class="controls "> <input class="numberinput form-control product_os_version_name" id="id_product_os_version_name" name="product_os_version_name" value={} step="any" type="number"> </div></div><div id="div_id_ios_version_name" class="form-group col-md-1 os_version_icon fadeIn animated" style="width:100px;"> <label for="id_ios_version_name" class="control-label ">
                                        iOS Version</label> <div class="controls "> <input class="ios_version_name numberinput form-control" value={} id="id_ios_version_name" name="ios_version_name" step="any" type="number"> </div> </div>
                                        <div class="col-md-1 remove"><a class="delete_product_row" href="javascript:void(0);"></a></div></div>
                        '''.format(product_select_list(ticket.product),product_version_select_list(ticket.product_version),product_os_version_select_list(ticket.product_os_version),ticket.product_os_version_name,ticket.ios_version_name))
                    else:
                        html = HTML('''
                            <div class="product_layout_div layout_sec"> <div id="div_id_product" class="form-group col-md-3 for-margin"> <label for="id_product" class="control-label  requiredField">
                                        Select Product<span class="star">*</span> </label> {} </div> <div id="div_id_product_version" class="form-group col-md-3 for-margin"> <label for="id_product_version" class="control-label  requiredField">
                                        Product Version<span class="star">*</span> </label> {} </div> <div id="div_id_product_os_version" class="form-group col-md-3 for-margin"> <label for="id_product_os_version" class="control-label  requiredField">
                                        Operating System<span class="star">*</span> </label> {} </div> <div id="div_id_product_os_version_name" class="form-group col-md-2 for-margin os_version_icon"> <label for="id_product_os_version_name" class="control-label  requiredField">
                                        OS Version<span class="star">*</span></label> <div class="controls "> <input class="numberinput form-control product_os_version_name" id="id_product_os_version_name" name="product_os_version_name" value={} step="any" type="number"> </div></div><div id="div_id_ios_version_name" class="form-group col-md-1 os_version_icon hidden fadeIn animated" style="width:100px;"> <label for="id_ios_version_name" class="control-label ">
                                        iOS Version</label> <div class="controls "> <input class="ios_version_name numberinput form-control"  id="id_ios_version_name" name="ios_version_name" step="any" type="number"> </div> </div>
                                        <div class="col-md-1 remove"><a class="delete_product_row" href="javascript:void(0);"></a></div></div>
                        '''.format(product_select_list(ticket.product),product_version_select_list(ticket.product_version),product_os_version_select_list(ticket.product_os_version),ticket.product_os_version_name))

                    self.uploaded_products_layout.append(
                        html
                    )
            # if self.instance.ticket_id.all():
            #     for ticket in self.instance.ticket_id.all():
            #         self.uploaded_classification_layout.append(
            #             HTML('''
            #                 <div class="gluu_layout_div"> <div id="div_id_gluu_server_version" class="form-group col-md-4"> <label for="id_gluu_server_version" class="control-label  requiredField">
            #                 Gluu Server Version<span class="star">*</span> </label> {} </div> <div id="div_id_os_version" class="form-group col-md-4"> <label for="id_os_version" class="control-label  requiredField">
            #                 Operating System<span class="star">*</span> </label> {} </div> <div id="div_id_os_version_name" class="form-group col-md-3 os_version_icon"> <label for="id_os_version_name" class="control-label  requiredField">
            #                 OS Version<span class="star">*</span> </label> <div class="controls "> <input class="numberinput form-control os_version_name" id="id_os_version_name" name="os_version_name" value={} step="any" type="number"> </div> </div>
            #                 <div class="col-md-1 remove"><a class="delete_gluu_row" href="javascript:void(0);"></a></div></div>
            #             '''.format(gluu_server_version_select_list (ticket.gluu_server_version),gluu_os_version_list(ticket.os_version),ticket.os_version_name)
            #                 )
            #         )

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal ticket_form'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            # self.uploaded_classification_layout,
            self.classification_layout,
            self.uploaded_products_layout,
            self.product_layout,
            self.description_layout,
            self.category_layout,
            self.additional_layout,
            self.button_layout
        )

    def clean_gluu_server_version_comments(self):

        if (self.cleaned_data.get('gluu_server_version') and
                self.cleaned_data.get('gluu_server_version') in ('N/A', 'Other')):

            if not self.cleaned_data.get('gluu_server_version_comments'):

                raise forms.ValidationError(_('Please specify the Gluu Server version'))

        return self.cleaned_data.get('gluu_server_version_comments')

    def clean_os_version_comments(self):

        if (self.cleaned_data.get('os_version') and
                self.cleaned_data.get('os_version') == 'Other'):

            if not self.cleaned_data.get('os_version_comments'):

                raise forms.ValidationError(_('Please specify the OS version'))

        return self.cleaned_data.get('os_version_comments')

    def clean_os_version_name(self):
        if not self.cleaned_data.get('os_version_name') or self.cleaned_data.get('os_version_name') < 0:
            raise forms.ValidationError(_('Please enter os version in positive numbers.'))
        return self.cleaned_data.get('os_version_name')

class NamedUserTicketForm(UserTicketForm):

    is_private = forms.ChoiceField(
        choices=constants.TICKET_PRIVACY,
        initial=True,
        label=_('Privacy'),
        required=False
    )

    issue_type = forms.ChoiceField(
        choices=constants.ISSUE_TYPE_CREATE,
        label=_('Issue Type')
    )

    attachment = forms.FileField(
        max_length=255,
        required=False
    )

    file_upload_layout = FieldWithButtons(Div('attachment', StrictButton(
        'Add new file',
        css_id='add_new_file',
        css_class='btn btn-xs btn-success'),
        css_class='full-wide layout_sec'),
    )

    fine_uploader_layout= Layout(

        Div(
            css_id= 'fine-uploader-manual-trigger',
            css_class= 'layout_sec'
        ),
    )


    uploaded_files_layout = Layout()

    class Meta(UserTicketForm.Meta):

        fields = UserTicketForm.Meta.fields + ('issue_type', 'is_private')

    def __init__(self, *args, **kwargs):

        super(NamedUserTicketForm, self).__init__(*args, **kwargs)
        forms.FileField(widget=forms.FileInput(attrs={'class': 'rounded_list'}))
        self.uploaded_files_layout = Layout()

        if self.instance and self.instance.issue_type:
            self.fields['issue_type'].choices = constants.ISSUE_TYPE
        else:
            self.fields['issue_type'].choices = constants.ISSUE_TYPE_CREATE

        if self.instance.id and self.instance.owned_by.is_basic:
            self.fields['issue_type'].required = False


        self.helper.layout = Layout(
            self.classification_layout,
            self.uploaded_products_layout,
            self.product_layout,
            self.category_layout,
            self.description_layout,
            self.additional_layout,
            self.fine_uploader_layout,
            # self.file_upload_layout,
            # self.uploaded_files_layout,
            self.button_layout
        )

    def clean_issue_type(self):
        if (self.cleaned_data.get('product') and
                 self.cleaned_data.get('product') in ('GLUU', 'OXD', 'SUP_GLUU') ):
            if not self.cleaned_data.get('issue_type'):
                raise forms.ValidationError(_('Please specify the issue type'))
        return self.cleaned_data.get('issue_type')

class StaffTicketForm(NamedUserTicketForm):

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label=_('Select a company'),
        label=_('Create ticket on behalf of')
    )

    created_for = forms.CharField(
        required=False,
        label=_('Open the ticket for'),
        widget=forms.Select(attrs={'class': 'chosen-select'}),
    )

    assigned_to = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(
            is_active=True,
            crm_type__in=[pc.STAFF, pc.ADMIN, pc.MANAGER]
        ),
        required=False,
        empty_label=_('Assign the ticket')
    )

    status = forms.ChoiceField(
        choices=constants.TICKET_STATUS_CREATE,
        initial='new',
        label=_('Status')
    )

    partner_layout = Layout(Div(
        Field('company',wrapper_class='col-md-6'),
        Field('created_for',wrapper_class='col-md-6'),css_class= 'layout_sec' #wrapper_class='hidden')
    ),)

    staff_layout = Layout(Div(
        Field('assigned_to', wrapper_class='col-md-6'),Field('status' ,wrapper_class='col-md-6'),css_class= 'layout_sec'
    ),)

    def clean_created_for(self):
        created_for = self.cleaned_data.get('created_for', None)

        if created_for and created_for != 'N/A':
            try:
                return UserProfile.objects.get(id=created_for)
            except ObjectDoesNotExist:
                pass

        return None

    def clean(self):

        cleaned_data = super(StaffTicketForm, self).clean()
        company = cleaned_data.get('company', None)
        created_for = cleaned_data.get('created_for', None)

        if company and not created_for:

            raise forms.ValidationError(
                'Please specify a user in the company you want to create an account for.')

    class Meta(NamedUserTicketForm.Meta):

        fields = NamedUserTicketForm.Meta.fields + ('status', 'assigned_to',)

    def __init__(self, *args, **kwargs):

        super(StaffTicketForm, self).__init__(*args, **kwargs)
        self.fields['product_os_version'].label = "Operating System"
        self.fields['product_os_version_name'].label = "OS Version"
        instance = kwargs.pop('instance', False)

        if instance:
            self.fields['status'].choices = constants.TICKET_STATUS

            if instance.created_for:

                self.fields['company'].initial = instance.company_association

                users = UserProfile.objects.filter(
                    company_association=instance.company_association)

                choices = [['N/A', 'Select a user in that company']]
                for user in users:
                    choices.append([user.id, user.get_full_name()])

                self.fields['created_for'].widget = forms.Select(
                    attrs={'class': 'chosen-select'},
                    choices=choices
                )

                self.fields['created_for'].initial = str(instance.created_for.id)

        self.helper.layout = Layout(
            self.partner_layout,
            self.classification_layout,
            self.uploaded_products_layout,
            self.product_layout,
            self.category_layout,
            self.description_layout,
            self.staff_layout,
            self.additional_layout,
            self.fine_uploader_layout,
            # self.file_upload_layout,
            # self.uploaded_files_layout,
            self.button_layout
        )


class PartnerTicketForm(NamedUserTicketForm):

    company = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label=_('Select a company'),
        label=_('Create ticket on behalf of')
    )

    created_for = forms.CharField(
        required=False,
        label=_(' '),
        widget=forms.Select(attrs={'class': 'chosen-select'}),
    )


    partner_layout = Layout(Div(
        Field('company',wrapper_class='col-md-6'),
        Field('created_for',wrapper_class='col-md-6'),css_class= 'layout_sec' #wrapper_class='hidden')
    ),)

    def __init__(self, clients, *args, **kwargs):

        super(PartnerTicketForm, self).__init__(*args, **kwargs)

        self.fields['company'].queryset = clients

        instance = kwargs.pop('instance', False)

        if instance and instance.company_association and instance.created_for:

            self.fields['company'].initial = instance.company_association
            users = UserProfile.objects.filter(company_association=instance.company_association)

            choices = [['N/A', 'Select a user in that company']]
            for user in users:
                choices.append([user.id, user.get_full_name()])

            self.fields['created_for'].widget = forms.Select(
                attrs={'class': 'chosen-select'},
                choices=choices
            )

            self.fields['created_for'].initial = str(instance.created_for.id)

        self.helper.layout = Layout(
            self.partner_layout,
            self.classification_layout,
            self.uploaded_products_layout,
            self.product_layout,
            self.category_layout,
            self.description_layout,
            self.additional_layout,
            self.fine_uploader_layout,
            self.button_layout,
        )

    def clean_created_for(self):
        created_for = self.cleaned_data.get('created_for', None)

        if created_for and created_for != 'N/A':
            try:
                return UserProfile.objects.get(id=created_for)
            except ObjectDoesNotExist:
                pass

        return None

    def clean(self):

        cleaned_data = super(PartnerTicketForm, self).clean()
        company = cleaned_data.get('company', None)
        created_for = cleaned_data.get('created_for', None)

        if company and not created_for:

            raise forms.ValidationError(
                'Please specify a user in the company you want to create an account for.')


class TicketInlineForm(forms.ModelForm):

    assigned_to = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(
            is_active=True,
            crm_type__in=[pc.STAFF, pc.ADMIN, pc.MANAGER]
        ),
        required=False,
        empty_label=_('Unassigned')
    )

    class Meta:

        model = Ticket
        error_css_class = 'error_form'
        fields = ['assigned_to', 'status']


class UserAnswerForm(forms.ModelForm):

    close_ticket = forms.BooleanField(
        required=False,
        label=_('Close this ticket')
    )

    additional_layout = Layout(
        Div(
            PrependedText(
                'link_url',
                '<span class="glyphicon glyphicon-link"></span>\
                 <span style="margin-left:3px;" title="Include an outside \
                 link to any relevant details." data-toggle="tooltip" \
                 class="glyphicon glyphicon-info-sign"></span>',
                placeholder='Video or screenshot url'
            ),
            PrependedText(
                'send_copy',
                '<span class="glyphicon glyphicon-envelope"></span>\
                 <span style="margin-left:3px;" title="Send a copy of \
                 this response to colleagues." \
                 data-toggle="tooltip" class="glyphicon glyphicon-info-sign"></span>',
                placeholder='Separate emails with commas'
            ),
        )
    )

    button_layout = Div(
        FormActions(
            Submit('save', 'Post'),
            Submit('close', 'Close', css_class='btn-danger')
            # Reset('name', 'Reset')
        )
    )
    button_layout_without_close = Div(
        FormActions(
            Submit('save', 'Post')
        )
    )
    class Meta:
        model = Answer
        error_css_class = 'error_form'
        fields = ['answer', 'link_url', 'send_copy']

    def __init__(self, *args, **kwargs):
        ticket = kwargs.pop('ticket', None)
        user = kwargs.pop('user', None)
        can_close = False

        if ticket and user and hasattr(ticket, 'has_edit_permission') and ticket.status != 'closed':
            can_close = ticket.has_edit_permission(user)

        super(UserAnswerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.attrs = {'onsubmit': 'save.disabled = true; return true;'}
        self.helper.form_class = 'form-horizontal answer_form'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.help_text_inline = True

        if can_close:
            self.helper.layout = Layout(
                Div(
                    Field('answer',placeholder="Enter your answer here"),
                    self.additional_layout,
                    Field('close_ticket',wrapper_class='hidden'),
                    self.button_layout
                )
            )
        else:
            self.helper.layout = Layout(
                Div(
                    Field('answer',placeholder="Enter your answer here"),
                    self.additional_layout,
                    self.button_layout_without_close
                )
            )


class NamedUserAnswerForm(UserAnswerForm):

    attachment = forms.FileField(
        max_length=255,
        required=False,
        label=_('Attachment')
    )

    file_upload_layout = FieldWithButtons('attachment', StrictButton(
        'Add new file',
        css_id='add_new_file',
        css_class='btn btn-xs btn-success pull-left')
    )

    class Meta(UserAnswerForm.Meta):

        fields = UserAnswerForm.Meta.fields + [
            'privacy', 'attachment'
        ]

    def __init__(self, *args, **kwargs):
        ticket = kwargs.pop('ticket', None)
        user = kwargs.pop('user', None)
        can_close = False

        if ticket and user and hasattr(ticket, 'has_edit_permission') and ticket.status != 'closed':
            can_close = ticket.has_edit_permission(user)

        super(NamedUserAnswerForm, self).__init__(*args, **kwargs)

        if can_close:
            if (ticket and user and ticket.owned_by == user) or (ticket and user and ticket.company_association == user.company_association):
                self.helper.layout = Layout(
                    Div(

                        Field('answer',placeholder="Enter your answer here"),
                        Field('privacy'),
                        self.additional_layout,
                        self.file_upload_layout,
                        Field('close_ticket', wrapper_class='hidden'),
                        self.button_layout
                    ),
                )
            else:
                self.helper.layout = Layout(
                    Div(

                        Field('answer',placeholder="Enter your answer here"),
                        Field('privacy',disabled="disabled"),
                        self.additional_layout,
                        self.file_upload_layout,
                        Field('close_ticket', wrapper_class='hidden'),
                        self.button_layout
                    ),
                )
        else:
            if (ticket and user and ticket.owned_by == user) or (ticket and user and ticket.company_association == user.company_association):
                self.helper.layout = Layout(
                    Div(

                        Field('answer',placeholder="Enter your answer here"),
                        Field('privacy'),
                        self.additional_layout,
                        self.file_upload_layout,
                        self.button_layout_without_close
                    ),
                )
            else:
                self.helper.layout = Layout(
                    Div(

                        Field('answer',placeholder="Enter your answer here"),
                        Field('privacy',disabled="disabled"),
                        self.additional_layout,
                        self.file_upload_layout,
                        self.button_layout_without_close
                    ),
                )

class StaffAnswerForm(NamedUserAnswerForm):

    status = forms.ChoiceField(
        choices=constants.TICKET_STATUS,
        required=False,
        label=_('Ticket status')
    )

    assigned_to_answer = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(
            is_active=True,
            crm_type__in=[pc.STAFF, pc.ADMIN, pc.MANAGER]
        ),
        required=False,
        label=_('Assigned to'),
        empty_label=_('Assign the ticket')
    )

    class Meta(NamedUserAnswerForm.Meta):

        fields = NamedUserAnswerForm.Meta.fields + ['status', 'privacy', 'attachment']

    def __init__(self, *args, **kwargs):

        self.ticket = kwargs.pop('ticket', False)
        user = kwargs.pop('user', None)
        super(StaffAnswerForm, self).__init__(*args, **kwargs)

        if self.ticket and self.ticket.assigned_to:
            self.fields['assigned_to_answer'].initial = self.ticket.assigned_to

        if self.ticket and self.ticket.status:
            self.fields['status'].initial = self.ticket.status
        can_close = False

        if self.ticket and user and hasattr(self.ticket, 'has_edit_permission') and self.ticket.status != 'closed':
            can_close = self.ticket.has_edit_permission(user)

        if can_close:
            self.helper.layout = Layout(
                Div(
                    Field(
                        'answer',
                        placeholder='Answer content',

                    ),
                    'assigned_to_answer',
                    'status',
                    'privacy',
                    self.additional_layout,
                    self.file_upload_layout,
                    Field('close_ticket', wrapper_class='hidden'),
                    self.button_layout
                ),
            )
        else:
            self.helper.layout = Layout(
                Div(
                    Field('answer',placeholder="Enter your answer here"),
                    'assigned_to_answer',
                    'status',
                    'privacy',
                    self.additional_layout,
                    self.file_upload_layout,
                    self.button_layout_without_close
                ),
            )

class AnswerInline(forms.Form):

    id = forms.IntegerField(required=True)
    answer = forms.CharField(required=True)


class DashboardInline(forms.Form):

    draw = forms.IntegerField(required=True)
    length = forms.IntegerField(required=True)
    start = forms.IntegerField(required=True)
    columns = forms.CharField(required=False)
    order = forms.CharField(required=False)
    search = forms.CharField(required=False)


class AssignInline(forms.Form):

    uid = forms.IntegerField(required=True)
    tid = forms.IntegerField(required=True)


class FilterTicketsForm(forms.Form):

    named = forms.BooleanField(
        required=False
    )

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(
            is_active=True, crm_type__in=[pc.STAFF, pc.ADMIN, pc.MANAGER]
        ),
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select',
            'data-placeholder': 'Select a staff member'
        }),
        required=False
    )

    category = forms.MultipleChoiceField(
        choices=constants.TICKET_CATEGORY,
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select',
            'data-placeholder': 'Select a category'
        }),
        required=False)

    status = forms.MultipleChoiceField(
        choices=constants.TICKET_STATUS_FILTER,
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select',
            'data-placeholder': 'Select a status'
        }),
        required=False)

    issue_type = forms.MultipleChoiceField(
        choices=constants.ISSUE_TYPE_FILTER,
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select',
            'data-placeholder': 'Select an issue type'
        }),
        required=False)

    created_filters = forms.ChoiceField(
        choices=constants.DATE_FILTER_TYPES,
        required=False
    )

    created_date = forms.DateField(
        required=False
    )

    company = forms.MultipleChoiceField(
        choices=sorted(set(UserProfile.objects.values_list('company', 'company').order_by('company'))),
        widget=forms.SelectMultiple(attrs={
            'class': 'cstmchosen',
            'data-placeholder': 'Select a company'
        }),
        required=False)

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super(FilterTicketsForm, self).__init__(*args, **kwargs)

        # Force reloading the choices manually, since automated reloaing appears to be too lazy
        self.fields['company'].choices = sorted(set(UserProfile.objects.values_list('company', 'company').order_by('company')))

        if user:

            if user.is_admin:

                choices_created_by = UserProfile.objects.filter(is_active=True)

            elif user.is_named:

                clients = Company.objects.filter(
                    clients__is_deleted=False,
                    clients__partner=user.company_association
                )

                q = [Q(is_active=True) & (
                     Q(company_association=user.company_association) |
                     Q(company_association__in=clients))]

                choices_created_by = UserProfile.objects.filter(*q)

            else:
                choices_created_by = UserProfile.objects.none()

            self.fields['created_by'] = forms.ModelMultipleChoiceField(
                queryset=choices_created_by,
                widget=forms.SelectMultiple(attrs={
                    'class': 'chosen-select',
                    'data-placeholder': 'Select a user'
                }),
                required=False)
