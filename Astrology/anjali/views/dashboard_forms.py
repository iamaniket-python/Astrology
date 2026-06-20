from django import forms
from ..models import (
    SiteSettings, About, AboutFeature, Service, AstrologyCourse,
    Gallery, Product, Testimonial,
)


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['name', 'heading', 'description', 'experience_years', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AboutFeatureForm(forms.ModelForm):
    class Meta:
        model = AboutFeature
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['icon', 'title', 'description', 'price', 'order', 'is_active']
        widgets = {
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AstrologyCourseForm(forms.ModelForm):
    class Meta:
        model = AstrologyCourse
        fields = [
            'title', 'description', 'level', 'duration', 'mode', 'students',
            'price', 'gradient', 'badge_bg', 'badge_color', 'order', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'mode': forms.TextInput(attrs={'class': 'form-control'}),
            'students': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'gradient': forms.TextInput(attrs={'class': 'form-control'}),
            'badge_bg': forms.TextInput(attrs={'class': 'form-control'}),
            'badge_color': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'emoji', 'image', 'gradient', 'span_two_columns', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'emoji': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gradient': forms.TextInput(attrs={'class': 'form-control'}),
            'span_two_columns': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'price', 'icon',
            'image', 'gradient', 'order', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gradient': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'city', 'message', 'emoji', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'emoji': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['location', 'phone', 'email', 'whatsapp_number']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
        }