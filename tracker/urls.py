from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_job_card, name='submit_job_card'),
    path('track/', views.track_job_card, name='track_job_card'),
    path('dashboard/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
]