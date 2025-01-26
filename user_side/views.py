from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from admin_side.models import Destination, Activity, Accommodation, Restaurant, Article, UploadedFile
from django.core.cache import cache
from django.views.generic import ListView, DetailView
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)



def search_api(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'destinations')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)

    results = []
    
    try:
        if category == 'destinations':
            items = Destination.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]
            model_type = 'Destination'
            
        elif category == 'activities':
            items = Activity.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]
            model_type = 'Activity'
            
        elif category == 'hotels':
            items = Accommodation.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]
            model_type = 'Hotel'
            
        elif category == 'restaurants':
            items = Restaurant.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]
            model_type = 'Restaurant'

        for item in items:
            results.append({
                'title': item.name,
                'description': item.description[:100] + '...' if len(item.description) > 100 else item.description,
                'image': item.image.url if hasattr(item, 'image') and item.image else None,
                'category': model_type,
                'url': item.get_absolute_url(),
            })

        return JsonResponse(results, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
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
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    ordering = ['-published_date']

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        print("Article Detail View Triggered")
        return super().get(request, *args, **kwargs)

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


def chatbot_file(request):
    chatbot_file_list = UploadedFile.objects.all()
    page = request.GET.get('page', 1)
    
    # Show 9 destinations per page
    paginator = Paginator(chatbot_file_list, 9)
    
    try:
        chatbot_file = paginator.page(page)
    except PageNotAnInteger:
        chatbot_file = paginator.page(1)
    except EmptyPage:
        chatbot_file = paginator.page(paginator.num_pages)

    return render(request, 'chatbot_file.html', {'chatbot_files': chatbot_file})
