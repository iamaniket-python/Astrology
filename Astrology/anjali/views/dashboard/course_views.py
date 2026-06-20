from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ..dashboard_forms import AstrologyCourseForm
from ...models import AstrologyCourse


@superuser_required
def course_list(request):
    courses = AstrologyCourse.objects.all().order_by('order')
    return render(request, 'adminpanel/course_list.html', {'courses': courses})


@superuser_required
def course_add(request):
    if request.method == "POST":
        form = AstrologyCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added.")
            return redirect('course_list')
    else:
        form = AstrologyCourseForm()
    return render(request, 'adminpanel/course_form.html', {'form': form})


@superuser_required
def course_edit(request, pk):
    course = get_object_or_404(AstrologyCourse, pk=pk)
    if request.method == "POST":
        form = AstrologyCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated.")
            return redirect('course_list')
    else:
        form = AstrologyCourseForm(instance=course)
    return render(request, 'adminpanel/course_form.html', {'form': form, 'course': course})


@superuser_required
def course_delete(request, pk):
    course = get_object_or_404(AstrologyCourse, pk=pk)
    course.delete()
    messages.success(request, "Course deleted.")
    return redirect('course_list')
