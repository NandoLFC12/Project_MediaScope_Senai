# Em analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard_home'),
    path('sentiment/', views.sentiment_analysis_view, name='sentiment_analysis'),
    # A rota 'settings' foi removida.
]