from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from admin_side.models import Destination, Activity, Accommodation
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def home(request):
    try:
        # Try to get all cached items
        cached_items = cache.get('random_homepage_items')
        
        if not cached_items:
            # If not cached, get new random items for each section
            cached_items = {}
            
            # Use select_related() to reduce database queries if you have foreign keys
            destinations =(Destination.objects.filter(
                image__isnull=False
            ).select_related().order_by('?')[:5])
            
            activities =(Activity.objects.filter(
                image__isnull=False
            ).select_related().order_by('?')[:5])
            
            if destinations or activities:  # Only cache if we have data
                cached_items = {
                    'random_destinations': destinations,
                    'random_activities': activities,
                }
                # Cache the results for 1 hour
                cache.set('random_homepage_items', cached_items, 3600)
            
    except Exception as e:
        logger.error(f"Error fetching random items: {str(e)}")
        cached_items = {
            'random_destinations': [],
            'random_activities': [],
        }

    # Add any additional context data needed by the template
    context = {
        'random_destinations': cached_items.get('random_destinations', []),
        'random_activities': cached_items.get('random_activities', []),
        'page_title': 'Home',  # Optional: Add page title
    }

    return render(request, 'home2.html', context)


def user_side_destination_list(request):
    destination_list = Destination.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(destination_list, 9)
    
    try:
        destinations = paginator.page(page)
    except PageNotAnInteger:
        destinations = paginator.page(1)
    except EmptyPage:
        destinations = paginator.page(paginator.num_pages)
    
    return render(request, 'destination.html', {'destinations': destinations})

def accommodation(request):
    accommodation_list = Accommodation.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(accommodation_list, 9)
    
    try:
        accommodation = paginator.page(page)
    except PageNotAnInteger:
        accommodation = paginator.page(1)
    except EmptyPage:
        accommodation = paginator.page(paginator.num_pages)

    return render(request, 'accomodation.html', {'accommodations': accommodation})


# def article(request):
#     return render(request, 'articles.html')

def food(request):
    food_list = Activity.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(food_list, 9)
    
    try:
        food = paginator.page(page)
    except PageNotAnInteger:
        food = paginator.page(1)
    except EmptyPage:
        food = paginator.page(paginator.num_pages)

    return render(request, 'food_drinks.html', {'foods': food})


# def attractions_view(request):
#     return render(request, 'admin_side/attractions.html')

# def food_view(request):
#     return render(request, 'admin_side/food.html')

def activity(request):
    activity_list = Activity.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(activity_list, 9)
    
    try:
        activity = paginator.page(page)
    except PageNotAnInteger:
        activity = paginator.page(1)
    except EmptyPage:
        activity = paginator.page(paginator.num_pages)

    return render(request, 'activity.html', {'activities': activity})

# def events_view(request):
#     return render(request, 'admin_side/events.html')


