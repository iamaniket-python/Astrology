from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ..dashboard_forms import AboutForm, AboutFeatureForm
from ...models import About, AboutFeature


@superuser_required
def about_edit(request):
    about, _ = About.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "About section updated.")
            return redirect('about_edit')
    else:
        form = AboutForm(instance=about)

    context = {'form': form, 'features': about.features.all()}
    return render(request, 'adminpanel/about_form.html', context)


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
            return redirect('about_edit')
    else:
        form = AboutFeatureForm()

    return render(request, 'adminpanel/about_feature_form.html', {'form': form})


@superuser_required
def about_feature_delete(request, pk):
    feature = get_object_or_404(AboutFeature, pk=pk)
    feature.delete()
    messages.success(request, "Feature deleted.")
    return redirect('about_edit')
