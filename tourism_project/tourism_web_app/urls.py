from django.urls import path
from . import views

urlpatterns = [
    path('tourism_web_app/', views.tourism_web_app, name='tourism_web_app'),
]