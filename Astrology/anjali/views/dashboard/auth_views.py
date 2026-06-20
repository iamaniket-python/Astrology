from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, 'adminpanel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')
