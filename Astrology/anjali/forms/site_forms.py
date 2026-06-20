from django import forms
from ..models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Interested In'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }