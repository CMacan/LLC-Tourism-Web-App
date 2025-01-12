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

    path('admin_food_drink/', views.admin_food_drink, name='admin_food_drink'),

    path('add-restaurant/', views.add_restaurant_entry, name='add_restaurant_entry'),

    path('admin_activity/', views.admin_activity, name='admin_activity'),
    path('admin_activity/add-activity/', views.add_activity, name='add_activity'),
    path('admin_side/list-activity/', views.activity_list, name='activity_list'),
    path('admin_activity/update/<int:id>/', views.update_activity, name='update_activity'),
    path('admin_activity/delete/<int:id>/', views.delete_activity, name='delete_activity'),
    path('admin_activity/get/<int:id>/', views.get_activity, name='get_activity'),

    path('admin_article/', views.admin_article, name='admin_article'),
]
