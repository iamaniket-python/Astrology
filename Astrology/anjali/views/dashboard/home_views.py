from django.shortcuts import render
from django.db.models import Count, Q

from .decorators import superuser_required
from ...models import Service, Product, AstrologyCourse, Testimonial, Gallery, ContactInquiry


@superuser_required
def dashboard(request):
    # FIX: was 7 separate .count() queries → now 1 aggregated query
    counts = ContactInquiry.objects.aggregate(
        total_inquiries=Count("id"),
        unread_inquiries=Count("id", filter=Q(is_read=False)),
    )

    context = {
        "total_services":    Service.objects.count(),
        "total_products":    Product.objects.count(),
        "total_courses":     AstrologyCourse.objects.count(),
        "total_testimonials": Testimonial.objects.count(),
        "total_gallery":     Gallery.objects.count(),
        "total_inquiries":   counts["total_inquiries"],
        "unread_inquiries":  counts["unread_inquiries"],
    }
    return render(request, "adminpanel/dashboard.html", context)
