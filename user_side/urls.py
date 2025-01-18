from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('activity/', views.activity, name='activity'),
    path('food/', views.food, name='food'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('destination/', views.user_side_destination_list, name='user_side_destination_list'),
]