from django import forms

from haystack.forms import SearchForm

from tickets.constants import TICKET_STATUS, TICKET_CATEGORY, GLUU_SERVER_VERSION, OS_VERSION


class TicketSearchForm(SearchForm):

    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        required=True,
    )

    category = forms.ChoiceField(
        choices=TICKET_CATEGORY,
        required=False,
        widget=forms.Select(attrs={'class': 'btn btn-default'})
    )

    status = forms.ChoiceField(
        choices=TICKET_STATUS,
        required=False,
        widget=forms.Select(attrs={'class': 'btn btn-default'})
    )

    server_version = forms.ChoiceField(
        choices=GLUU_SERVER_VERSION,
        required=False,
        widget=forms.Select(attrs={'class': 'btn btn-default'})
    )

    os_version = forms.ChoiceField(
        choices=OS_VERSION,
        required=False,
        widget=forms.Select(attrs={'class': 'btn btn-default'})
    )
