from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.base import ContentFile

from .decorators import superuser_required
from ..forms.dashboard_forms import ProductForm
from ..models import Product

from PIL import Image as PilImage
import io


def compress_image(image_field, max_width=600, quality=75):
    """Resize + compress product image (products are small cards, 600px enough)."""
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

    original_name = getattr(image_field, "name", "product.jpg")
    base_name     = original_name.rsplit(".", 1)[0]
    return ContentFile(buffer.read(), name=f"{base_name}.jpg")


@superuser_required
def product_list(request):
    products = Product.objects.all().order_by("order")
    return render(request, "adminpanel/product_list.html", {"products": products})


@superuser_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if "image" in request.FILES:
                instance.image = compress_image(request.FILES["image"])
            instance.save()
            messages.success(request, "Product added.")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "adminpanel/product_form.html", {"form": form})


@superuser_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            instance = form.save(commit=False)
            if "image" in request.FILES:
                instance.image = compress_image(request.FILES["image"])
            instance.save()
            messages.success(request, "Product updated.")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "adminpanel/product_form.html", {"form": form, "product": product})


@superuser_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect("product_list")
