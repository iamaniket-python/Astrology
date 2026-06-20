from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from dashboard_forms import ProductForm
from ...models import Product


@superuser_required
def product_list(request):
    products = Product.objects.all().order_by('order')
    return render(request, 'adminpanel/product_list.html', {'products': products})


@superuser_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added.")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'adminpanel/product_form.html', {'form': form})


@superuser_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminpanel/product_form.html', {'form': form, 'product': product})


@superuser_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect('product_list')
