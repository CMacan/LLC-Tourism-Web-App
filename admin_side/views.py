from django.shortcuts import render, redirect 
from .models import Restaurant
from .models import Destination
from django.http import HttpResponse
from django.http import JsonResponse


def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html', {
        'page_title': 'Dashboard'
    })

# DESTINATIONS
def admin_destination(request):
    destinations = Destination.objects.all()  # Check if this is correct
    return render(request, 'admin_destination.html', {'destinations': destinations})


def add_destination_entry(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        category = request.POST.get('category')
        rating = request.POST.get('rating')
        popular = request.POST.get('popular') == 'on'  # Handle checkbox
        image = request.FILES.get('image')  # Handle image upload

        # Create and save the destination
        destination = Destination.objects.create(
            name=name,
            location=location,
            description=description,
            category=category,
            rating=rating,
            popular=popular,
            image=image
        )

        # Return a response to indicate success (optional)
        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'error'}, status=400)

def destination_list(request):
    destinations = Destination.objects.all()  # Fetch all destinations from the database
    return render(request, 'admin_destination.html', {'destinations': destinations})


# ACCOMMODATIONS 
def admin_accomodation(request):
    return render(request, 'admin_accomodation.html', {
        'page_title': 'Accommodations'
    })


# RESTAURANTS
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

def restaurant_list(request):
    # Fetch all restaurants from the database
    restaurants = Restaurant.objects.all()
    return render(request, 'admin_destination.html', {'restaurants': restaurants})

# ARTICLES
def admin_article(request):
    return render(request, 'admin_article.html', {
        'page_title': 'Articles'
    })

# ACTIVITIES
def admin_activities(request):
    return render(request, 'admin_activities.html', {
        'page_title': 'Activities'
    })