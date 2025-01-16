from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('activities/', views.activities_view, name='activities_view'),
    path('food/', views.food, name='food'),
    path('articles/', views.article, name='articles'),
    path('destination/', views.destination_list, name='destination_list'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
]