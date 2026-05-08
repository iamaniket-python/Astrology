from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    Service,
    AstrologyCourse,
    Product,
    Testimonial,
)

from .forms import ContactInquiryForm


def index(request):

    # Fetch Dynamic Data
    services = Service.objects.filter(is_active=True)
    courses = AstrologyCourse.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)

    # Contact Form
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your consultation request has been submitted successfully."
            )

            return redirect('index')

    else:
        form = ContactInquiryForm()

    context = {
        "services": services,
        "courses": courses,
        "products": products,
        "testimonials": testimonials,
        "form": form,
    }

    return render(request, "User/index.html", context)