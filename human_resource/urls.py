from django.urls import path

from . import views

urlpatterns = [
    path('opportunities/', views.opportunities, name='opportunities'),
    path('support/', views.support, name='support'),
    path('frontend_email/', views.frontend_email, name='frontend_email'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/<int:pk>/',
         views.delete_message, name='delete_message'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_vacancy/', views.edit_vacancy, name='edit_vacancy'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message, name='message'),
    path('mark_as_read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('edit_countdown/', views.edit_countdown, name='edit_countdown'),
    path('autologout/', views.autologout, name='autologout'),
    path('waiting/', views.waiting, name='waiting'),
    path('candidates/', views.candidates, name='candidates'),
    path('candidate/<int:id>/', views.candidate, name='candidate'),
    path('candidate/<int:id>/delete/',
         views.delete_candidate, name='delete_candidate'),
    path('export/<int:id>/', views.export_to_pdf, name='export_to_pdf'),
    path('pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('application/', views.application, name='application'),
    path('', views.home, name='home'),
]
