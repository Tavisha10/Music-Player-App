# App/urls.py (app-level)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),            # your main player view
    path('register/', views.register_view, name='register'),
    # Add other app URLs here (upload, detail, api endpoints, etc.)
]
