from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ..dashboard_forms import GalleryForm
from ...models import AstrologyCourse, Gallery


@superuser_required
def gallery_list(request):
    items = Gallery.objects.all().order_by('order')
    return render(request, 'adminpanel/gallery_list.html', {'items': items})


@superuser_required
def gallery_add(request):
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo added to gallery.")
            return redirect('gallery_list')
    else:
        form = GalleryForm()
    return render(request, 'adminpanel/gallery_form.html', {'form': form})


@superuser_required
def gallery_edit(request, pk):
    item = get_object_or_404(Gallery, pk=pk)
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo updated.")
            return redirect('gallery_list')
    else:
        form = GalleryForm(instance=item)
    return render(request, 'adminpanel/gallery_form.html', {'form': form, 'item': item})


@superuser_required
def gallery_delete(request, pk):
    item = get_object_or_404(Gallery, pk=pk)
    item.delete()
    messages.success(request, "Photo deleted.")
    return redirect('gallery_list')
