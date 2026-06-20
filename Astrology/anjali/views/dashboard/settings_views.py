from django.shortcuts import render, redirect
from django.contrib import messages

from .decorators import superuser_required
from dashboard_forms import SiteSettingsForm
from ...models import SiteSettings


@superuser_required
def settings_edit(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated.")
            return redirect('settings_edit')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    return render(request, 'adminpanel/settings_form.html', {'form': form})
