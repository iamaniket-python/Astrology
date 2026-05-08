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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Service,
    Product,
    AstrologyCourse,
    Testimonial,
    Gallery,
    ContactInquiry
)


# ================= LOGIN =================

def admin_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'adminpanel/login.html')


# ================= DASHBOARD =================

@login_required(login_url='admin_login')
def dashboard(request):

    context = {
        'total_services': Service.objects.count(),
        'total_products': Product.objects.count(),
        'total_courses': AstrologyCourse.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_gallery': Gallery.objects.count(),
        'total_inquiries': ContactInquiry.objects.count(),
    }

    return render(request, 'adminpanel/dashboard.html', context)


# ================= LOGOUT =================

def admin_logout(request):
    logout(request)
    return redirect('admin_login')