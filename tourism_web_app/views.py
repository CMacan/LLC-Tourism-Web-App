from django.shortcuts import render
from django.http import HttpResponse

def home(request):
<<<<<<< HEAD:tourism_project/tourism_web_app/views.py
    return render(request, 'home.html')

def destination(request):
    return render(request, 'destination.html')
=======
    return render(request, 'index.html')
>>>>>>> origin/melchor-branch:tourism_web_app/views.py
