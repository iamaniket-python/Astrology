from django import forms
from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):

    class Meta:
        model = ContactInquiry
        fields = [
            'full_name',
            'phone',
            'email',
            'service',
            'message'
        ]

        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5
            })
        }