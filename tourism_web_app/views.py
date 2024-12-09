from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'torism2.html')


def home2(request):
    return render(request, 'torism.html')