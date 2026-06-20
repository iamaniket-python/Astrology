from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .decorators import superuser_required
from ...models import ContactInquiry


@superuser_required
def inquiry_list(request):
    inquiries = ContactInquiry.objects.all().order_by('-submitted_at')
    return render(request, 'adminpanel/inquiry_list.html', {'inquiries': inquiries})


@superuser_required
def inquiry_mark_read(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    inquiry.is_read = True
    inquiry.save(update_fields=['is_read'])
    messages.success(request, "Marked as read.")
    return redirect('inquiry_list')


@superuser_required
def inquiry_delete(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    inquiry.delete()
    messages.success(request, "Inquiry deleted.")
    return redirect('inquiry_list')
