"""Forms for estimates app"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from django.utils.translation import gettext_lazy as _

from .models import Estimate


class EstimateCreateForm(forms.ModelForm):
    """Form for creating an estimate (checkout)"""

    class Meta:
        model = Estimate
        fields = ['client_name', 'client_email', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('client_name', css_class='form-group col-md-6 mb-0'),
                Column('client_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('notes', css_class='form-group'),
            Submit('submit', _('Request Estimate'), css_class='btn btn-primary btn-lg')
        )


class GuestCheckoutForm(forms.Form):
    """Form for guest users to provide contact information at checkout"""
    company_name = forms.CharField(
        max_length=255,
        required=True,
        label=_("Company Name"),
        widget=forms.TextInput(attrs={'placeholder': 'Your Company Name'})
    )
    contact_person = forms.CharField(
        max_length=255,
        required=True,
        label=_("Contact Person"),
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        required=True,
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label=_("Phone Number"),
        widget=forms.TextInput(attrs={'placeholder': '(555) 123-4567'})
    )
    client_name = forms.CharField(
        max_length=255,
        required=False,
        label=_("Client/Homeowner Name"),
        widget=forms.TextInput(attrs={'placeholder': 'Optional'})
    )
    client_email = forms.EmailField(
        required=False,
        label=_("Client Email"),
        widget=forms.EmailInput(attrs={'placeholder': 'Optional'})
    )
    notes = forms.CharField(
        required=False,
        label=_("Additional Notes"),
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any special requirements or notes'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-3'),
                Column('contact_person', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('client_name', css_class='form-group col-md-6 mb-3'),
                Column('client_email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('notes', css_class='form-group mb-3'),
            Submit('submit', _('Request Estimate'), css_class='btn btn-primary btn-lg')
        )
