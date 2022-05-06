from django.urls import path

from . import views

urlpatterns = [
    path('opportunities/', views.opportunities, name='opportunities'),
    path('frontend_email/', views.frontend_email, name='frontend_email'),
    path('backend_email/', views.backend_email, name='backend_email'),
    path('', views.home, name='home'),
]
