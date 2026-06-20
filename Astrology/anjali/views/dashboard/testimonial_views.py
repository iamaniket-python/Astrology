from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ..dashboard_forms import TestimonialForm
from ...models import Testimonial


@superuser_required
def testimonial_list(request):
    testimonials = Testimonial.objects.all().order_by('order')
    return render(request, 'adminpanel/testimonial_list.html', {'testimonials': testimonials})


@superuser_required
def testimonial_add(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added.")
            return redirect('testimonial_list')
    else:
        form = TestimonialForm()
    return render(request, 'adminpanel/testimonial_form.html', {'form': form})


@superuser_required
def testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated.")
            return redirect('testimonial_list')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'adminpanel/testimonial_form.html', {'form': form, 'testimonial': testimonial})


@superuser_required
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, "Testimonial deleted.")
    return redirect('testimonial_list')
