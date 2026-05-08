from django import forms
from .models import ContactInquiry, Service


class ContactInquiryForm(forms.ModelForm):

    # Dynamically populate service choices from the DB
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label="— Select a Service —",
        to_field_name="title",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = ContactInquiry
        fields = ("name", "phone", "email", "service", "message")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your full name",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+91 XXXXX XXXXX",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us what you need help with…",
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        digits = phone.replace("+", "").replace(" ", "").replace("-", "")
        if not digits.isdigit():
            raise forms.ValidationError("Enter a valid phone number.")
        if len(digits) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_service(self):
        # Store the service title string, not the object
        service_obj = self.cleaned_data.get("service")
        return service_obj.title if service_obj else ""