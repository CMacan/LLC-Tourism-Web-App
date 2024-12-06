from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def destination(request):
    return render(request, 'destination.html')