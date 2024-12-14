from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def acc(request):
    return render(request, 'accomodation.html')

