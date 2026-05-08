from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    SiteSettings, About, AboutFeature,
    Service, AstrologyCourse, Gallery,
    Product, Testimonial, ContactInquiry,
)
from .dashboard_forms import (
    SiteSettingsForm, AboutForm, AboutFeatureFormSet,
    ServiceForm, AstrologyCoursesForm, GalleryForm,
    ProductForm, TestimonialForm,
)


# ════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        error = "Invalid credentials or not a superuser."

    return render(request, 'adminpanel/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ════════════════════════════════════════════════
# DASHBOARD HOME
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def dashboard(request):
    context = {
        'total_services':     Service.objects.count(),
        'total_products':     Product.objects.count(),
        'total_courses':      AstrologyCourse.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_gallery':      Gallery.objects.count(),
        'total_inquiries':    ContactInquiry.objects.count(),
        'unread_inquiries':   ContactInquiry.objects.filter(is_read=False).count(),
        'recent_inquiries':   ContactInquiry.objects.order_by('-submitted_at')[:5],
    }
    return render(request, 'adminpanel/dashboard.html', context)


# ════════════════════════════════════════════════
# SITE SETTINGS
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def settings_edit(request):
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Site settings updated successfully.')
        return redirect('settings_edit')
    return render(request, 'adminpanel/settings.html', {'form': form})


# ════════════════════════════════════════════════
# ABOUT
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def about_edit(request):
    obj, _ = About.objects.get_or_create(pk=1)
    form    = AboutForm(request.POST or None, request.FILES or None, instance=obj)
    formset = AboutFeatureFormSet(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, 'About section updated.')
        return redirect('about_edit')
    return render(request, 'adminpanel/about.html', {'form': form, 'formset': formset})


# ════════════════════════════════════════════════
# SERVICES
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def services_list(request):
    return render(request, 'adminpanel/services.html', {
        'items': Service.objects.all().order_by('-id')
    })

@login_required(login_url='admin_login')
def service_add(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service added.')
        return redirect('services_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Add Service', 'back_url': 'services_list'
    })

@login_required(login_url='admin_login')
def service_edit(request, pk):
    obj  = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Service updated.')
        return redirect('services_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Edit Service', 'back_url': 'services_list'
    })

@login_required(login_url='admin_login')
def service_delete(request, pk):
    get_object_or_404(Service, pk=pk).delete()
    messages.success(request, 'Service deleted.')
    return redirect('services_list')


# ════════════════════════════════════════════════
# COURSES
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def courses_list(request):
    return render(request, 'adminpanel/courses.html', {
        'items': AstrologyCourse.objects.all().order_by('-id')
    })

@login_required(login_url='admin_login')
def course_add(request):
    form = AstrologyCoursesForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course added.')
        return redirect('courses_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Add Course', 'back_url': 'courses_list'
    })

@login_required(login_url='admin_login')
def course_edit(request, pk):
    obj  = get_object_or_404(AstrologyCourse, pk=pk)
    form = AstrologyCoursesForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course updated.')
        return redirect('courses_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Edit Course', 'back_url': 'courses_list'
    })

@login_required(login_url='admin_login')
def course_delete(request, pk):
    get_object_or_404(AstrologyCourse, pk=pk).delete()
    messages.success(request, 'Course deleted.')
    return redirect('courses_list')


# ════════════════════════════════════════════════
# GALLERY
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def gallery_list(request):
    return render(request, 'adminpanel/gallery.html', {
        'items': Gallery.objects.all().order_by('-id')
    })

@login_required(login_url='admin_login')
def gallery_add(request):
    form = GalleryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gallery item added.')
        return redirect('gallery_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Add Gallery Item', 'back_url': 'gallery_list'
    })

@login_required(login_url='admin_login')
def gallery_edit(request, pk):
    obj  = get_object_or_404(Gallery, pk=pk)
    form = GalleryForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gallery item updated.')
        return redirect('gallery_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Edit Gallery Item', 'back_url': 'gallery_list'
    })

@login_required(login_url='admin_login')
def gallery_delete(request, pk):
    get_object_or_404(Gallery, pk=pk).delete()
    messages.success(request, 'Gallery item deleted.')
    return redirect('gallery_list')


# ════════════════════════════════════════════════
# PRODUCTS
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def products_list(request):
    return render(request, 'adminpanel/products.html', {
        'items': Product.objects.all().order_by('-id')
    })

@login_required(login_url='admin_login')
def product_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product added.')
        return redirect('products_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Add Product', 'back_url': 'products_list'
    })

@login_required(login_url='admin_login')
def product_edit(request, pk):
    obj  = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('products_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Edit Product', 'back_url': 'products_list'
    })

@login_required(login_url='admin_login')
def product_delete(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    messages.success(request, 'Product deleted.')
    return redirect('products_list')


# ════════════════════════════════════════════════
# TESTIMONIALS
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def testimonials_list(request):
    return render(request, 'adminpanel/testimonials.html', {
        'items': Testimonial.objects.all().order_by('-id')
    })

@login_required(login_url='admin_login')
def testimonial_add(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial added.')
        return redirect('testimonials_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Add Testimonial', 'back_url': 'testimonials_list'
    })

@login_required(login_url='admin_login')
def testimonial_edit(request, pk):
    obj  = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial updated.')
        return redirect('testimonials_list')
    return render(request, 'adminpanel/form.html', {
        'form': form, 'title': 'Edit Testimonial', 'back_url': 'testimonials_list'
    })

@login_required(login_url='admin_login')
def testimonial_delete(request, pk):
    get_object_or_404(Testimonial, pk=pk).delete()
    messages.success(request, 'Testimonial deleted.')
    return redirect('testimonials_list')


# ════════════════════════════════════════════════
# INQUIRIES
# ════════════════════════════════════════════════

@login_required(login_url='admin_login')
def inquiries_list(request):
    items = ContactInquiry.objects.all().order_by('-submitted_at')
    return render(request, 'adminpanel/inquiries.html', {'items': items})

@login_required(login_url='admin_login')
def inquiry_detail(request, pk):
    obj = get_object_or_404(ContactInquiry, pk=pk)
    if not obj.is_read:
        obj.is_read = True
        obj.save(update_fields=['is_read'])
    return render(request, 'adminpanel/inquiry_detail.html', {'obj': obj})

@login_required(login_url='admin_login')
def inquiry_delete(request, pk):
    get_object_or_404(ContactInquiry, pk=pk).delete()
    messages.success(request, 'Inquiry deleted.')
    return redirect('inquiries_list')

@login_required(login_url='admin_login')
@require_POST
def inquiry_mark_read(request, pk):
    """Toggle read/unread status — callable via AJAX or plain POST."""
    obj = get_object_or_404(ContactInquiry, pk=pk)
    obj.is_read = not obj.is_read
    obj.save(update_fields=['is_read'])
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_read': obj.is_read})
    return redirect('inquiries_list')

@login_required(login_url='admin_login')
@require_POST
def inquiries_mark_all_read(request):
    """Bulk-mark every unread inquiry as read."""
    ContactInquiry.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'All inquiries marked as read.')
    return redirect('inquiries_list')