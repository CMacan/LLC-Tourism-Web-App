from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path("upload_file/", views.upload_file_view, name="upload_file"),
]
