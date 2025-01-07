from django.shortcuts import render, redirect 
from .models import Restaurant
from django.http import HttpResponse


def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html', {
        'page_title': 'Dashboard'
    })

def admin_destination(request):
    return render(request, 'admin_destination.html', {
        'page_title': 'Destinations'
    })

def admin_accomodation(request):
    return render(request, 'admin_accomodation.html', {
        'page_title': 'Accommodations'
    })

def admin_food_drink(request):
    return render(request, 'admin_food_drink.html', {
        'page_title': 'Food & Drinks'
    })

def add_restaurant_entry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        cuisine_type = request.POST.get('cuisine_type')
        photo = request.FILES.get('photo')  # Handle the uploaded photo

        # Save the new restaurant entry
        Restaurant.objects.create(
            name=name,
            address=address,
            contact_number=contact_number,
            cuisine_type=cuisine_type,
            photo=photo
        )
        return redirect('admin_food_drink')  # Redirect to your admin page
    return HttpResponse(status=400)

def admin_article(request):
    return render(request, 'admin_article.html', {
        'page_title': 'Articles'
    })

def admin_activities(request):
    return render(request, 'admin_activities.html', {
        'page_title': 'Activities'
    })