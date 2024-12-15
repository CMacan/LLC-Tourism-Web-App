from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('activity/', views.activity, name='activity'),
    path('food/', views.food, name='food'),
    path('articles/', views.article, name='articles'),
    path('destination/', views.destination, name='destination'),
]