from django.shortcuts import render, redirect,  get_object_or_404
from .models import Restaurant, Destination, Activity, Accommodation
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import logging


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



# RESTAURANTS
def admin_food_drink(request):
    return render(request, 'admin_food_drink.html', {
        'page_title': 'Food & Drinks'
    })


@ensure_csrf_cookie
def restaurant_list(request):
    restaurants = Restaurant.objects.all().order_by('-1')
    return render(request, 'admin_side/admin_food_drink.html', {'restaurants': restaurants})


logger = logging.getLogger(__name__)

@csrf_exempt
def create_restaurant(request):
    if request.method == 'POST':
        try:
            # Log incoming data for debugging
            logger.debug(f"POST data: {request.POST}")
            logger.debug(f"FILES data: {request.FILES}")

            # Create restaurant object
            restaurant = Restaurant.objects.create(
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                price_range=request.POST.get('pricePerNight'),
                contact_num=request.Post.get('contactNumber'),
                rating=request.POST.get('rating') if request.POST.get('rating') else None,
                website=request.POST.get('websiteURL'),
            )

            # Handle photo upload
            if 'image' in request.FILES:
                restaurant.photo = request.FILES['image']
                restaurant.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Restaurant created successfully',
                'id': restaurant.id
            })

        except Exception as e:
            logger.error(f"Error creating restaurant: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


@csrf_exempt
def update_restaurant(request, id):
    if request.method == 'POST':
        try:
            restaurant = get_object_or_404(Restaurant, id=id)
            data = json.loads(request.POST.get('data'))
            
            restaurant.name = data['name']
            restaurant.address = data['address']
            restaurant.cuisine_type = data.get('cuisine_type')
            restaurant.rating = data.get('rating') if data.get('rating') else None
            restaurant.price_range = data.get('price_range')
            restaurant.opening_hours = data.get('opening_hours')
            restaurant.website = data.get('website')
            restaurant.contact_number = data.get('contact_number')
            restaurant.menu_url = data.get('menu_url')
            restaurant.is_open = data.get('is_open', True)
            
            if 'photo' in request.FILES:
                restaurant.photo = request.FILES['photo']
            
            restaurant.save()
            
            return JsonResponse({'status': 'success', 'message': 'Restaurant updated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def delete_restaurant(request, id):
    if request.method == 'POST':
        try:
            restaurant = get_object_or_404(Restaurant, id=id)
            restaurant.delete()
            return JsonResponse({'status': 'success', 'message': 'Restaurant deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def get_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'cuisine_type': restaurant.cuisine_type,
        'rating': str(restaurant.rating) if restaurant.rating else None,
        'price_range': restaurant.price_range,
        'opening_hours': restaurant.opening_hours,
        'website': restaurant.website,
        'contact_number': restaurant.contact_number,
        'menu_url': restaurant.menu_url,
        'is_open': restaurant.is_open,
        'photo_url': restaurant.photo.url if restaurant.photo else None
    }
    return JsonResponse(data)


# ARTICLES
def admin_article(request):
    return render(request, 'admin_article.html', {
        'page_title': 'Articles'
    })

# ACTIVITIES
def admin_activity(request):
    activities = Activity.objects.all().order_by('-created_at')  # Add ordering if desired
    return render(request, 'admin_activity.html', {
        'activities': activities,
        'page_title': 'Activities'
    })


@require_http_methods(["POST"])
def add_activity(request):
    try:
        print("Received POST data:", request.POST)
        print("Received FILES:", request.FILES)
        
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        # Validate required fields
        if not all([name, description, category]):
            return JsonResponse({
                'success': False,
                'message': 'Missing required fields'
            }, status=400)

        # Create activity object
        activity = Activity.objects.create(
            name=name,
            description=description,
            category=category,
            price=price if price else None,
            image=image if image else None
        )

        return JsonResponse({
            'success': True, 
            'message': 'Activity added successfully',
            'id': activity.id
        })
        
    except Exception as e:
        import traceback
        print("Error:", str(e))
        print("Traceback:", traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


def activity_list(request):
    activity = Activity.objects.all().order_by('-id')  # Most recent first
    return render(request, 'admin_side/admin_activity.html', {
        'activities': activity
    })

def get_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
        data = {
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'category': activity.category,
            'rating': activity.rating,
        }
        return JsonResponse(data)
    except Activity.DoesNotExist:
        return JsonResponse({'error': 'Activity not found'}, status=404)


@require_http_methods(["POST"])
def update_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
        
        # Update text fields
        activity.name = request.POST.get('name')
        activity.location = request.POST.get('location')
        activity.description = request.POST.get('description')
        activity.category = request.POST.get('category')
        activity.rating = request.POST.get('rating')
        activity.popular = request.POST.get('popular') == 'on'
        
        # Handle image update
        if 'image' in request.FILES:
            # Delete old image if it exists
            if activity.image:
                if os.path.isfile(activity.image.path):
                    os.remove(activity.image.path)
            activity.image = request.FILES['image']
        
        activity.save()
        return JsonResponse({'success': True, 'message': 'Activity updated successfully'})
    except Activity.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Activity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["POST"])
def delete_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
        activity.delete()
        return JsonResponse({'success': True, 'message': 'Activity deleted successfully'})
    except Activity.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Activity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def admin_accomodation(request):
    accommodation = Accommodation.objects.all().order_by('-created_at')  # Add ordering if desired
    return render(request, 'admin_accomodation.html', {
        'accommodations': accommodation,
    })


def accommodation_list(request):
    accommodations = Accommodation.objects.all().order_by('-created_at')
    return render(request, 'admin/accommodation_list.html', {'accommodations': accommodations})

@csrf_exempt
def create_accommodation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data'))
            image = request.FILES.get('image')
            
            accommodation = Accommodation.objects.create(
                name=data['name'],
                address=data['address'],
                price_per_night=data['price_per_night'],
                description=data['description'],
                rating=data.get('rating'),
                website=data.get('website'),
                image=image
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Accommodation created successfully',
                'id': accommodation.id
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def update_accommodation(request, id):
    if request.method == 'POST':
        try:
            accommodation = get_object_or_404(Accommodation, id=id)
            data = json.loads(request.POST.get('data'))
            
            accommodation.name = data['name']
            accommodation.address = data['address']
            accommodation.price_per_night = data['price_per_night']
            accommodation.description = data['description']
            accommodation.rating = data.get('rating')
            accommodation.website = data.get('website')
            
            if 'image' in request.FILES:
                accommodation.image = request.FILES['image']
            
            accommodation.save()
            
            return JsonResponse({'status': 'success', 'message': 'Accommodation updated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def delete_accommodation(request, id):
    if request.method == 'POST':
        try:
            accommodation = get_object_or_404(Accommodation, id=id)
            accommodation.delete()
            return JsonResponse({'status': 'success', 'message': 'Accommodation deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def get_accommodation(request, id):
    accommodation = get_object_or_404(Accommodation, id=id)
    data = {
        'id': accommodation.id,
        'name': accommodation.name,
        'address': accommodation.address,
        'price_per_night': str(accommodation.price_per_night),
        'description': accommodation.description,
        'rating': str(accommodation.rating) if accommodation.rating else None,
        'website': accommodation.website if accommodation.website else None,
        'image_url': accommodation.image.url if accommodation.image else None
    }
    return JsonResponse(data)