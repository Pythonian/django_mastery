from django.urls import path

from . import views

urlpatterns = [
    path('opportunities/', views.opportunities, name='opportunities'),
    path('', views.home, name='home'),
]
