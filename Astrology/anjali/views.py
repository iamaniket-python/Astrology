from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactInquiryForm
from .models import (
    About,
    Gallery,
    Service,
    AstrologyCourse,
    Product,
    Testimonial,
    SiteSettings,
)


def index(request):

    # ── Static / singleton data ──────────────────────────────────────────
    about = About.objects.first()
    about_features = about.features.all() if about else []
    site_settings = SiteSettings.objects.first()

    # ── Dynamic section data ─────────────────────────────────────────────
    services      = Service.objects.filter(is_active=True)
    courses       = AstrologyCourse.objects.filter(is_active=True)
    products      = Product.objects.filter(is_active=True)
    testimonials  = Testimonial.objects.filter(is_active=True)
    gallery_items = Gallery.objects.all()

    # ── Contact form ─────────────────────────────────────────────────────
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your consultation request has been submitted successfully."
            )
            return redirect("index")

    else:
        form = ContactInquiryForm()

    # ── Context ──────────────────────────────────────────────────────────
    context = {
        # About
        "about":          about,
        "about_features": about_features,

        # Site-wide
        "site_settings":  site_settings,

        # Sections
        "services":       services,
        "courses":        courses,
        "products":       products,
        "testimonials":   testimonials,
        "gallery_items":  gallery_items,

        # Form
        "form":           form,
    }

    return render(request, "User/index.html", context)