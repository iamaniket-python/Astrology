from django.shortcuts import render

from .decorators import superuser_required
from ...models import Service, Product, AstrologyCourse, Testimonial, Gallery, ContactInquiry


@superuser_required
def dashboard(request):
    context = {
        'total_services': Service.objects.count(),
        'total_products': Product.objects.count(),
        'total_courses': AstrologyCourse.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_gallery': Gallery.objects.count(),
        'total_inquiries': ContactInquiry.objects.count(),
        'unread_inquiries': ContactInquiry.objects.filter(is_read=False).count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)
