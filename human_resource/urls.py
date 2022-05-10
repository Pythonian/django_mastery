from django.urls import path

from . import views

urlpatterns = [
    path('opportunities/', views.opportunities, name='opportunities'),
    path('support/', views.support, name='support'),
    path('frontend_email/', views.frontend_email, name='frontend_email'),
    path('backend_email/', views.backend_email, name='backend_email'),
    path('send_message/', views.send_message, name='send_message'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('faq/', views.faq, name='faq'),
    path('edit_vacancy/', views.edit_vacancy, name='edit_vacancy'),
    path('inbox/', views.inbox, name='inbox'),
    path('edit_countdown/', views.edit_countdown, name='edit_countdown'),
    path('', views.home, name='home'),
]
