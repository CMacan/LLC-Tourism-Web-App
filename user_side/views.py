from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def accommodation(request):
    return render(request, 'accomodation.html')

def activity(request):
    return render(request, 'activity.html')

def destination(request):
    return render(request, 'destination.html')

def article(request):
    return render(request, 'articles.html')

def food(request):
    return render(request, 'food_drinks.html')

