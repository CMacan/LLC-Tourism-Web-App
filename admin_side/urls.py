from django.urls import path
from . import views

urlpatterns = [
    path('login2/', views.login2, name='login2'),
    path('login/', views.login_user, name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('admin_destination/', views.admin_destination, name='admin_destination'),
    path('admin_destination/add-destination/', views.add_destination, name='add_destination'),
    path('admin_destination/list-destination/', views.destination_list, name='destination_list'),
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
    path('admin_activity/list-activity/', views.activity_list, name='activity_list'),
    path('admin_activity/update/<int:id>/', views.update_activity, name='update_activity'),
    path('admin_activity/delete/<int:id>/', views.delete_activity, name='delete_activity'),
    path('admin_activity/get/<int:id>/', views.get_activity, name='get_activity'),


    path('admin_articles/', views.admin_articles, name='admin_article'),
    path('admin_articles/<int:id>/', views.article_detail, name='article_detail'),
    path('admin_articles/create/', views.create_article, name='create_article'),
    path('admin_articles/<int:id>/update/', views.update_article, name='update_article'),
    path('admin_articles/<int:id>/delete/', views.delete_article, name='delete_article'),

    path('admin_chatbot_file/', views.admin_chatbot_file, name='admin_chatbot_file'),
    path('admin_chatbot_file/add-chatbot_file/', views.add_chatbot_file, name='add_chatbot_file'),
    path('admin_chatbot_file/list-chatbot_file/', views.chatbot_file_list, name='chatbot_file_list'),
    path('admin_chatbot_file/delete/<int:id>/', views.delete_chatbot_file, name='delete_activity'),
    path('admin_chatbot_file/get/<int:id>/', views.get_chatbot_file, name='get_chatbot_file'),
]
