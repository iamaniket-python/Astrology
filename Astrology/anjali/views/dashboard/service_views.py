from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ..dashboard_forms import ServiceForm
from ...models import Service


@superuser_required
def service_list(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'adminpanel/service_list.html', {'services': services})


@superuser_required
def service_add(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added.")
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'adminpanel/service_form.html', {'form': form})


@superuser_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated.")
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'adminpanel/service_form.html', {'form': form, 'service': service})


@superuser_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, "Service deleted.")
    return redirect('service_list')
