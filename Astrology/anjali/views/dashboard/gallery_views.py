from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.base import ContentFile

from .decorators import superuser_required
from ..dashboard_forms import GalleryForm
from ...models import Gallery

from PIL import Image as PilImage
import io


def compress_image(image_field, max_width=1000, quality=75):
    """Resize + compress uploaded image to reduce storage & load time."""
    img = PilImage.open(image_field)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    if img.width > max_width:
        ratio = max_width / img.width
        new_h = int(img.height * ratio)
        img   = img.resize((max_width, new_h), PilImage.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)

    original_name = getattr(image_field, "name", "gallery.jpg")
    base_name     = original_name.rsplit(".", 1)[0]
    return ContentFile(buffer.read(), name=f"{base_name}.jpg")


@superuser_required
def gallery_list(request):
    items = Gallery.objects.all().order_by("order")
    return render(request, "adminpanel/gallery_list.html", {"items": items})


@superuser_required
def gallery_add(request):
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if "image" in request.FILES:
                instance.image = compress_image(request.FILES["image"])
            instance.save()
            messages.success(request, "Photo added to gallery.")
            return redirect("gallery_list")
    else:
        form = GalleryForm()
    return render(request, "adminpanel/gallery_form.html", {"form": form})


@superuser_required
def gallery_edit(request, pk):
    item = get_object_or_404(Gallery, pk=pk)
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            instance = form.save(commit=False)
            if "image" in request.FILES:
                instance.image = compress_image(request.FILES["image"])
            instance.save()
            messages.success(request, "Photo updated.")
            return redirect("gallery_list")
    else:
        form = GalleryForm(instance=item)
    return render(request, "adminpanel/gallery_form.html", {"form": form, "item": item})


@superuser_required
def gallery_delete(request, pk):
    item = get_object_or_404(Gallery, pk=pk)
    item.delete()
    messages.success(request, "Photo deleted.")
    return redirect("gallery_list")
