from django import forms
from django.forms import inlineformset_factory

from .models import (
    SiteSettings, About, AboutFeature,
    Service, AstrologyCourse, Gallery,
    Product, Testimonial,
)


# ════════════════════════════════════════════════
# SHARED WIDGET HELPERS
# ════════════════════════════════════════════════

TEXT_INPUT   = forms.TextInput(attrs={'class': 'form-control'})
EMAIL_INPUT  = forms.EmailInput(attrs={'class': 'form-control'})
NUMBER_INPUT = forms.NumberInput(attrs={'class': 'form-control'})
TEXTAREA     = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
FILE_INPUT   = forms.ClearableFileInput(attrs={'class': 'form-control'})
SELECT       = forms.Select(attrs={'class': 'form-select'})
CHECKBOX     = forms.CheckboxInput(attrs={'class': 'form-check-input'})


# ════════════════════════════════════════════════
# SITE SETTINGS
# ════════════════════════════════════════════════

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model  = SiteSettings
        fields = '__all__'
        widgets = {
            'site_name':        TEXT_INPUT,
            'tagline':          TEXT_INPUT,
            'email':            EMAIL_INPUT,
            'phone':            TEXT_INPUT,
            'address':          TEXTAREA,
            'facebook_url':     TEXT_INPUT,
            'instagram_url':    TEXT_INPUT,
            'youtube_url':      TEXT_INPUT,
            'twitter_url':      TEXT_INPUT,
            'whatsapp_number':  TEXT_INPUT,
            'logo':             FILE_INPUT,
            'favicon':          FILE_INPUT,
            'meta_description': TEXTAREA,
            'meta_keywords':    TEXT_INPUT,
        }


# ════════════════════════════════════════════════
# ABOUT
# ════════════════════════════════════════════════

class AboutForm(forms.ModelForm):
    class Meta:
        model  = About
        fields = '__all__'
        widgets = {
            'heading':          TEXT_INPUT,
            'subheading':       TEXT_INPUT,
            'description':      TEXTAREA,
            'experience_years': NUMBER_INPUT,
            'image':            FILE_INPUT,
            'video_url':        TEXT_INPUT,
        }


class AboutFeatureForm(forms.ModelForm):
    class Meta:
        model  = AboutFeature
        fields = ['icon', 'title', 'description', 'order']
        widgets = {
            'icon':        TEXT_INPUT,
            'title':       TEXT_INPUT,
            'description': TEXTAREA,
            'order':       NUMBER_INPUT,
        }


AboutFeatureFormSet = inlineformset_factory(
    About,
    AboutFeature,
    form=AboutFeatureForm,
    extra=1,
    can_delete=True,
)


# ════════════════════════════════════════════════
# SERVICE
# ════════════════════════════════════════════════

class ServiceForm(forms.ModelForm):
    class Meta:
        model  = Service
        fields = '__all__'
        widgets = {
            'title':       TEXT_INPUT,
            'slug':        TEXT_INPUT,
            'icon':        TEXT_INPUT,
            'short_desc':  TEXTAREA,
            'description': TEXTAREA,
            'image':       FILE_INPUT,
            'price':       NUMBER_INPUT,
            'is_active':   CHECKBOX,
            'order':       NUMBER_INPUT,
        }


# ════════════════════════════════════════════════
# ASTROLOGY COURSE
# ════════════════════════════════════════════════

class AstrologyCoursesForm(forms.ModelForm):
    class Meta:
        model  = AstrologyCourse
        fields = '__all__'
        widgets = {
            'title':        TEXT_INPUT,
            'slug':         TEXT_INPUT,
            'description':  TEXTAREA,
            'duration':     TEXT_INPUT,
            'level':        SELECT,
            'price':        NUMBER_INPUT,
            'discount_price': NUMBER_INPUT,
            'image':        FILE_INPUT,
            'is_active':    CHECKBOX,
            'is_featured':  CHECKBOX,
            'order':        NUMBER_INPUT,
        }


# ════════════════════════════════════════════════
# GALLERY
# ════════════════════════════════════════════════

class GalleryForm(forms.ModelForm):
    class Meta:
        model  = Gallery
        fields = '__all__'
        widgets = {
            'title':     TEXT_INPUT,
            'image':     FILE_INPUT,
            'category':  TEXT_INPUT,
            'is_active': CHECKBOX,
            'order':     NUMBER_INPUT,
        }


# ════════════════════════════════════════════════
# PRODUCT
# ════════════════════════════════════════════════

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = '__all__'
        widgets = {
            'name':           TEXT_INPUT,
            'slug':           TEXT_INPUT,
            'description':    TEXTAREA,
            'price':          NUMBER_INPUT,
            'discount_price': NUMBER_INPUT,
            'stock':          NUMBER_INPUT,
            'image':          FILE_INPUT,
            'category':       TEXT_INPUT,
            'is_active':      CHECKBOX,
            'is_featured':    CHECKBOX,
            'order':          NUMBER_INPUT,
        }


# ════════════════════════════════════════════════
# TESTIMONIAL
# ════════════════════════════════════════════════

class TestimonialForm(forms.ModelForm):
    class Meta:
        model  = Testimonial
        fields = '__all__'
        widgets = {
            'client_name':  TEXT_INPUT,
            'designation':  TEXT_INPUT,
            'review':       TEXTAREA,
            'rating':       SELECT,
            'image':        FILE_INPUT,
            'is_active':    CHECKBOX,
            'order':        NUMBER_INPUT,
        }