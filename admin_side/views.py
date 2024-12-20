from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def admin_destination(request):
    return render(request, 'admin_destination.html')