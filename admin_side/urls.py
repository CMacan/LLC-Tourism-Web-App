from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_destination/', views.admin_destination, name='admin_destination'),
    path('add-destination/', views.add_destination_entry, name='add_destination_entry'),
    path('list-destination/', views.destination_list, name='destination_list'),

    path('admin_accomodation/', views.admin_accomodation, name='admin_accomodation'),

    path('admin_food_drink/', views.admin_food_drink, name='admin_food_drink'),

    path('add-restaurant/', views.add_restaurant_entry, name='add_restaurant_entry'),

    path('admin_activities/', views.admin_activities, name='admin_activities'),
    
    path('admin_article/', views.admin_article, name='admin_article'),
]
