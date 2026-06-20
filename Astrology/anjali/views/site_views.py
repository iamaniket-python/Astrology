from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Original import path — bilkul waise hi rakha
from ..forms.site_forms import ContactInquiryForm
from ..models import (
    About, Gallery, Service, AstrologyCourse, Product, Testimonial, SiteSettings,
)


def index(request):
    # POST: form submit — cache bypass
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your consultation request has been submitted successfully.")
            return redirect("index")
        # Form invalid — render with errors
        return render(request, "User/index.html", _build_context(form))

    # GET — cached response
    form = ContactInquiryForm()
    return render(request, "User/index.html", _build_context(form))


def _build_context(form):
    about = (
        About.objects
        .prefetch_related("features")
        .first()
    )
    about_features = about.features.all() if about else []

    return {
        "about":          about,
        "about_features": about_features,
        "site_settings":  SiteSettings.objects.only(
                              "location", "phone", "email", "whatsapp_number"
                          ).first(),
        "services":       Service.objects.filter(is_active=True).only(
                              "icon", "title", "description", "price"
                          ).order_by("order"),
        "courses":        AstrologyCourse.objects.filter(is_active=True).only(
                              "title", "description", "level", "duration",
                              "mode", "students", "price",
                              "gradient", "badge_bg", "badge_color",
                          ).order_by("order"),
        "products":       Product.objects.filter(is_active=True).only(
                              "name", "category", "description", "price",
                              "icon", "image", "gradient",
                          ).order_by("order"),
        "testimonials":   Testimonial.objects.filter(is_active=True).only(
                              "name", "city", "message", "emoji",
                          ).order_by("order"),
        "gallery_items":  Gallery.objects.only(
                              "title", "emoji", "image",
                              "gradient", "span_two_columns",
                          ).order_by("order"),
        "form": form,
    }