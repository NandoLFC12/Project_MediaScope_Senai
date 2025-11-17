from django.urls import path
from . import views

urlpatterns = [
    # ... suas outras rotas ...
    path('login/', views.AuthView.as_view(), name='login'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/delete/', views.delete_account_view, name='delete_account'),
    
    # NOVA ROTA:
    path('settings/disconnect-google/', views.disconnect_google_view, name='disconnect_google'),
]