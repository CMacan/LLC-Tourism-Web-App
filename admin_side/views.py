from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import Restaurant, Destination, Activity, Accommodation, Article, Tag, User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
import os, random, hashlib, json, logging
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings



logger = logging.getLogger(__name__)

def login2(request):
    if request.session.get('user_id'):
        return redirect('dashboard')
    return render(request, 'login2.html')

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
               
            user = User.objects.filter(username=username).first()
            
            if user:
                print(f"\nFound user: {user.username}")
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                print(f"Input hash: {input_hash}")
                print(f"Stored hash: {user.password}")
                
                if user.password == input_hash:
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return JsonResponse({'message': 'Login successful'})
                else:
                    return JsonResponse({'error': 'Invalid password'}, status=400)
            else:
                return JsonResponse({'error': 'User does not exist'}, status=400)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'error': 'User with this email does not exist'}, status=400)

            # Generate new random password
            new_password = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                k=12
            ))
            
            # Hash and save new password
            user.password = hashlib.sha256(new_password.encode()).hexdigest()
            user.save()

            # Send email with new password
            try:
                send_mail(
                    subject="Password Reset",
                    message=f"Your new password is: {new_password}\nPlease change it after logging in.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return JsonResponse({'message': 'New password has been sent to your email'})
            except Exception as e:
                return JsonResponse({'error': f"Failed to send email: {str(e)}"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def logout_user(request):
    request.session.flush()
    return redirect('login2')


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
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        description = request.POST.get('description')
        category = request.POST.get('category')
        rating = request.POST.get('rating')
        popular = request.POST.get('popular') == 'on'
        image = request.FILES.get('image')

        # Create your destination object
        destination = Destination.objects.create(
            name=name,
            location=location,
            latitude=latitude,
            longitude=longitude,
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
            'latitude': destination.latitude,
            'longitude': destination.longitude,
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
        destination.latitude = request.POST.get('latitude')
        destination.longitude = request.POST.get('longitude')
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
    # Get all restaurants and pass them to the template
    restaurants = Restaurant.objects.all().order_by('-created_at')  # or any field you want to sort by
    return render(request, 'admin_food_drink.html', {
        'page_title': 'Food & Drinks',
        'restaurants': restaurants
    })


@ensure_csrf_cookie
def create_restaurant(request):
    if request.method == 'POST':
        try:
            # Print received data for debugging
            print("Received POST data:", request.POST)
            print("Received FILES:", request.FILES)

            # Validate required fields
            required_fields = ['name', 'address', 'facebook', 'instagram']
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValidationError(f'{field} is required')

            # Create new restaurant
            restaurant = Restaurant.objects.create(
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                facebook_link=request.POST.get('facebook'),
                instagram_link=request.POST.get('instagram'),
                website=request.POST.get('website', ''),
                rating=request.POST.get('rating', 0.0),
            )

            # Handle image
            if 'image' in request.FILES:
                print("Processing image upload...")
                image_file = request.FILES['image']
                print(f"Image file name: {image_file.name}")
                restaurant.image = image_file
                restaurant.save()
                print(f"Image saved. URL: {restaurant.image.url}")

            return JsonResponse({
                'status': 'success',
                'message': 'Restaurant added successfully',
                'restaurant': {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'facebook_link': restaurant.facebook_link,
                    'instagram_link': restaurant.instagram_link,
                    'website': restaurant.website,
                    'rating': float(restaurant.rating),
                    'image_url': restaurant.image.url if restaurant.image else None,
                }
            })

        except ValidationError as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({
                'status': 'error',
                'message': f'Server error: {str(e)}'
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def restaurant_list(request):
    restaurant = Restaurant.objects.all().order_by('-created_at')  # Add ordering if desired
    return render(request, 'admin_food_drink.html', {
        'restaurant': restaurant,
        'page_title': 'Restaurant'
    })

@require_http_methods(["GET"])
def get_restaurant(request, restaurant_id):
    try:
        print(f"Fetching restaurant with ID: {restaurant_id}")  # Debug print
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        data = {
            'status': 'success',
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'facebook': restaurant.facebook_link,  # Match the form field names
                'instagram': restaurant.instagram_link,  # Match the form field names
                'website': restaurant.website or '',
                'rating': str(restaurant.rating) if restaurant.rating is not None else '0',
                'image_url': restaurant.image.url if restaurant.image else None
            }
        }
        print(f"Returning data: {data}")  # Debug print
        return JsonResponse(data)
        
    except Restaurant.DoesNotExist:
        print(f"Restaurant {restaurant_id} not found")  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': f'Restaurant with ID {restaurant_id} not found'
        }, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)  # Changed to 500 for server errors

@require_http_methods(["POST"])
def update_restaurant(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        # Update fields
        restaurant.name = request.POST.get('name', restaurant.name)
        restaurant.address = request.POST.get('address', restaurant.address)
        restaurant.facebook_link = request.POST.get('facebook', restaurant.facebook_link)
        restaurant.instagram_link = request.POST.get('instagram', restaurant.instagram_link)
        restaurant.website = request.POST.get('website', restaurant.website)
        restaurant.rating = request.POST.get('rating', restaurant.rating)

        # Handle image update
        if 'image' in request.FILES:
            # Delete old image if it exists
            if restaurant.image:
                restaurant.image.delete()
            restaurant.image = request.FILES['image']

        restaurant.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Restaurant updated successfully',
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'facebook_link': restaurant.facebook_link,
                'instagram_link': restaurant.instagram_link,
                'website': restaurant.website,
                'rating': float(restaurant.rating),
                'image_url': restaurant.image.url if restaurant.image else None,
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["DELETE"])
def delete_restaurant(request, restaurant_id):
    try:
        # Print for debugging
        print(f"Attempting to delete restaurant with ID: {restaurant_id}")
        
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        restaurant_name = restaurant.name  # Store name before deletion
        
        # Delete the restaurant
        restaurant.delete()
        
        # Print success message
        print(f"Successfully deleted restaurant: {restaurant_name}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Restaurant {restaurant_name} deleted successfully'
        })
    except Restaurant.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Restaurant with ID {restaurant_id} not found'
        }, status=404)
    except Exception as e:
        print(f"Error deleting restaurant: {str(e)}")  # Print error for debugging
        return JsonResponse({
            'status': 'error',
            'message': 'Error deleting restaurant'
        }, status=400)

# ARTICLES
def ensure_default_tags():
    default_tags = [
        'Travel', 'Tips', 'Beach', 'Adventure', 'Food',
        'Culture', 'Nature', 'City', 'History', 'Photography'
    ]
    
    for tag_name in default_tags:
        Tag.objects.get_or_create(name=tag_name)


def admin_articles(request):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(request, 'admin_article.html', {'articles': articles, 'tags': tags})

@csrf_exempt
def article_detail(request, id):
    try:
        article = get_object_or_404(Article, id=id)
        if request.method == 'GET':
            return JsonResponse({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': article.author,
                'image_url': article.image.url if article.image else None,
                'tags': list(article.tags.values('id', 'name'))
            })
        else:
            return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def create_article(request):
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            content = request.POST.get('content')
            author = request.POST.get('author')
            image = request.FILES.get('image')
            tag_ids = request.POST.getlist('tags')

            # Validate required fields
            if not all([title, content, author]):
                return JsonResponse({
                    'error': 'Title, content, and author are required'
                }, status=400)

            # Create article
            article = Article.objects.create(
                title=title,
                content=content,
                author=author,
                image=image if image else None
            )

            # Add tags
            if tag_ids:
                tags = Tag.objects.filter(id__in=tag_ids)
                article.tags.set(tags)

            return JsonResponse({
                'message': 'Article created successfully',
                'id': article.id
            })

        except Exception as e:
            print(f"Error creating article: {str(e)}")  # Debug log
            return JsonResponse({
                'error': 'Error creating article'
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_http_methods(["POST"])
def update_article(request, id):
    try:
        # Debug logging
        logger.info(f"Received update request for article {id}")
        logger.info(f"POST data: {request.POST}")
        logger.info(f"FILES data: {request.FILES}")

        # Get the article
        article = get_object_or_404(Article, id=id)
        
        # Validate required fields
        required_fields = ['title', 'content', 'author']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)

        try:
            # Update basic fields
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.author = request.POST.get('author')

            if 'image' in request.FILES:
                if article.image:
                    article.image.delete(save=False)
                article.image = request.FILES['image']

            # Handle tags
            if 'tags' in request.POST:
                tags = request.POST.getlist('tags')
                article.tags.set(tags)

            # Save the article
            article.save()

            # Prepare success response
            response_data = {
                'message': 'Article updated successfully',
                'article': {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'author': article.author,
                    'image': article.image.url if article.image else None,
                    'tags': list(article.tags.values('id', 'name'))
                }
            }

            logger.info(f"Successfully updated article {id}")
            return JsonResponse(response_data)

        except Exception as e:
            logger.error(f"Error saving article data: {str(e)}")
            return JsonResponse({
                'error': f'Error saving article: {str(e)}'
            }, status=500)

    except Article.DoesNotExist:
        logger.error(f"Article {id} not found")
        return JsonResponse({
            'error': 'Article not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'error': f'Server error: {str(e)}'
        }, status=500)

@csrf_exempt
def delete_article(request, id):
    if request.method == 'DELETE':
        try:
            article = get_object_or_404(Article, id=id)
            article.delete()
            return JsonResponse({'message': 'Article deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponseBadRequest("Invalid HTTP method.")

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
        address = request.POST.get('address')
        description = request.POST.get('description')
        category = request.POST.get('category')
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
            address=address if address else None,
            description=description,
            category=category,
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
            'address': activity.address,
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
        activity.address = request.POST.get('address')
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