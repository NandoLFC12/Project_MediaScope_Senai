# Em subscriptions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('planos/', views.planos_view, name='planos'),
    
    # Rota que processa o clique no botão
    path('upgrade/<int:plan_id>/', views.upgrade_plan_view, name='upgrade_plan'),
]