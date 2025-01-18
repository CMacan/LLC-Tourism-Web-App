from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin_destination/', views.admin_destination, name='admin_destination'),
    path('admin_destination/add-destination/', views.add_destination, name='add_destination'),
    path('admin_side/list-destination/', views.destination_list, name='destination_list'),
    path('admin_destination/update/<int:id>/', views.update_destination, name='update_destination'),
    path('admin_destination/delete/<int:id>/', views.delete_destination, name='delete_destination'),
    path('admin_destination/get/<int:id>/', views.get_destination, name='get_destination'),

    path('admin_accomodation/', views.admin_accomodation, name='admin_accomodation'),
    path('accommodations/', views.accommodation_list, name='accommodation_list'),
    path('accommodations/create/', views.create_accommodation, name='create_accommodation'),
    path('accommodations/<int:id>/update/', views.update_accommodation, name='update_accommodation'),
    path('accommodations/<int:id>/delete/', views.delete_accommodation, name='delete_accommodation'),
    path('accommodations/<int:id>/', views.get_accommodation, name='get_accommodation'),

    

    path('admin_food_drink/', views.admin_food_drink, name='admin_food_drink'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/create/', views.create_restaurant, name='create_restaurant'),
    path('restaurants/delete/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('restaurants/<int:restaurant_id>/', views.get_restaurant, name='get_restaurant'),
    path('restaurants/update/<int:restaurant_id>/', views.update_restaurant, name='update_restaurant'),


    path('admin_activity/', views.admin_activity, name='admin_activity'),
    path('admin_activity/add-activity/', views.add_activity, name='add_activity'),
    path('admin_side/list-activity/', views.activity_list, name='activity_list'),
    path('admin_activity/update/<int:id>/', views.update_activity, name='update_activity'),
    path('admin_activity/delete/<int:id>/', views.delete_activity, name='delete_activity'),
    path('admin_activity/get/<int:id>/', views.get_activity, name='get_activity'),


    path('articles/', views.admin_article, name='admin_article'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:id>/update/', views.update_article, name='update_article'),
    path('articles/<int:id>/delete/', views.delete_article, name='delete_article'),
]
