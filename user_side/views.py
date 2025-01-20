from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from admin_side.models import Destination, Activity, Accommodation, Restaurant, Article
from django.core.cache import cache
from django.views.generic import ListView, DetailView
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
            destinations = Destination.objects.filter(
                image__isnull=False
            ).select_related().order_by('?')[:5]
            
            activities = Activity.objects.filter(
                image__isnull=False
            ).select_related().order_by('?')[:5]
            
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

    # Fetch the latest articles to display as featured blog posts
    featured_articles = Article.objects.all().order_by('-published_date')[:3]  # Get 3 latest articles

    # Add any additional context data needed by the template
    context = {
        'random_destinations': cached_items.get('random_destinations', []),
        'random_activities': cached_items.get('random_activities', []),
        'featured_articles': featured_articles,  # Add featured articles here
        'page_title': 'Home',  # Optional: Add page title
    }

    return render(request, 'home.html', context)

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


class ArticleListView(ListView):
    model = Article
    template_name = 'user_articles_list.html'
    context_object_name = 'articles'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'user_article_detail.html'
    context_object_name = 'article'

def food(request):
    restaurant_list = Restaurant.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(restaurant_list, 9)
    
    try:
        restaurant = paginator.page(page)
    except PageNotAnInteger:
        restaurant = paginator.page(1)
    except EmptyPage:
        restaurant = paginator.page(paginator.num_pages)

    return render(request, 'food_drinks.html', {'restaurants': restaurant})


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


