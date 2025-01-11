from django.shortcuts import render, redirect 
from .models import Restaurant
from .models import Destination
from .forms import DestinationForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import os


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


@require_http_methods(["POST"])
def add_destination(request):
    try:
        # Get form data
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        category = request.POST.get('category')
        rating = request.POST.get('rating')
        popular = request.POST.get('popular') == 'on'
        image = request.FILES.get('image')

        # Create your destination object
        destination = Destination.objects.create(
            name=name,
            location=location,
            description=description,
            category=category,
            rating=rating,
            popular=popular,
            image=image
        )

        return JsonResponse({'success': True, 'message': 'Destination added successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def destination_list(request):
    destinations = Destination.objects.all().order_by('-id')  # Most recent first
    return render(request, 'admin_side/admin_destination.html', {
        'destinations': destinations
    })

def get_destination(request, id):
    try:
        destination = Destination.objects.get(id=id)
        data = {
            'id': destination.id,
            'name': destination.name,
            'location': destination.location,
            'description': destination.description,
            'category': destination.category,
            'rating': destination.rating,
            'popular': destination.popular,
        }
        return JsonResponse(data)
    except Destination.DoesNotExist:
        return JsonResponse({'error': 'Destination not found'}, status=404)


@require_http_methods(["POST"])
def update_destination(request, id):
    try:
        destination = Destination.objects.get(id=id)
        
        # Update text fields
        destination.name = request.POST.get('name')
        destination.location = request.POST.get('location')
        destination.description = request.POST.get('description')
        destination.category = request.POST.get('category')
        destination.rating = request.POST.get('rating')
        destination.popular = request.POST.get('popular') == 'on'
        
        # Handle image update
        if 'image' in request.FILES:
            # Delete old image if it exists
            if destination.image:
                if os.path.isfile(destination.image.path):
                    os.remove(destination.image.path)
            destination.image = request.FILES['image']
        
        destination.save()
        return JsonResponse({'success': True, 'message': 'Destination updated successfully'})
    except Destination.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Destination not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["POST"])
def delete_destination(request, id):
    try:
        destination = Destination.objects.get(id=id)
        destination.delete()
        return JsonResponse({'success': True, 'message': 'Destination deleted successfully'})
    except Destination.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Destination not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)



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