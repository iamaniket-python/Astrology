from django.urls import path
from .views import index
from Astrology.anjali import views

urlpatterns = [
    path('', index, name='index'),
    
]