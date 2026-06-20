from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ...forms.site_forms import ContactInquiryForm  
from ...models import (
    About, Gallery, Service, AstrologyCourse, Product, Testimonial, SiteSettings,
)


# ── Cache homepage for 5 minutes (GET only) ──────────────────────────────────
# POST requests (form submit) bypass cache automatically via the view logic.
@cache_page(60 * 5)
def index(request):
    # POST: never use cached response — handle form first, then redirect
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your consultation request has been submitted successfully.")
            return redirect("index")
        # Form invalid — fall through to render with errors (no cache)
        _context = _build_context(form)
        return render(request, "User/index.html", _context)

    # GET — this response IS cached for 5 min
    form = ContactInquiryForm()
    return render(request, "User/index.html", _build_context(form))


def _build_context(form):
    """
    Single function builds all context.
    Uses .only() to fetch only needed fields → smaller rows, faster queries.
    Uses prefetch_related for about.features → 1 query instead of N.
    Uses select_related where FK joins help.
    """
    about = (
        About.objects
        .prefetch_related("features")   # avoids extra query per feature
        .first()
    )
    about_features = about.features.all() if about else []

    context = {
        "about":          about,
        "about_features": about_features,

        # .only() → fetch only columns the template actually uses
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
    return context
