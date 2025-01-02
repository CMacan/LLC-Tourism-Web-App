from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def admin_destination(request):
    return render(request, 'admin_destination.html')

def admin_accomodation(request):
    return render(request, 'admin_accomodation.html')

def admin_food_drink(request):
    return render(request, 'admin_food_drink.html')

def admin_article(request):
    return render(request, 'admin_article.html')

def admin_activities(request):
    return render(request, 'admin_activities.html')