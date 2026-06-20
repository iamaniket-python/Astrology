from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.base import ContentFile

from .decorators import superuser_required
from ..dashboard_forms import AboutForm, AboutFeatureForm
from ...models import About, AboutFeature

from PIL import Image as PilImage
import io


def compress_image(image_field, max_width=800, quality=75):
    """
    Resize + compress uploaded image.
    max_width=800px, quality=75 → ~70-80% smaller file size.
    Returns a ContentFile ready to assign back to the field.
    """
    img = PilImage.open(image_field)

    # Convert RGBA / palette to RGB (JPEG doesn't support transparency)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize only if wider than max_width (maintains aspect ratio)
    if img.width > max_width:
        ratio  = max_width / img.width
        new_h  = int(img.height * ratio)
        img    = img.resize((max_width, new_h), PilImage.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)

    # Build a clean filename
    original_name = getattr(image_field, "name", "image.jpg")
    base_name     = original_name.rsplit(".", 1)[0]
    new_name      = f"{base_name}_compressed.jpg"

    return ContentFile(buffer.read(), name=new_name)


@superuser_required
def about_edit(request):
    about, _ = About.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            instance = form.save(commit=False)

            # FIX: Compress image before saving if a new one was uploaded
            if "image" in request.FILES:
                instance.image = compress_image(request.FILES["image"])

            instance.save()
            messages.success(request, "About section updated.")
            return redirect("about_edit")
    else:
        form = AboutForm(instance=about)

    context = {"form": form, "features": about.features.all()}
    return render(request, "adminpanel/about_form.html", context)


@superuser_required
def about_feature_add(request):
    about, _ = About.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = AboutFeatureForm(request.POST)
        if form.is_valid():
            feature = form.save(commit=False)
            feature.about = about
            feature.save()
            messages.success(request, "Feature added.")
            return redirect("about_edit")
    else:
        form = AboutFeatureForm()

    return render(request, "adminpanel/about_feature_form.html", {"form": form})


@superuser_required
def about_feature_delete(request, pk):
    feature = get_object_or_404(AboutFeature, pk=pk)
    feature.delete()
    messages.success(request, "Feature deleted.")
    return redirect("about_edit")
