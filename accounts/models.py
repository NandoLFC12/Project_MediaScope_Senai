# Em accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django_countries.fields import CountryField
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário customizado unificado.
    """

    
    # --- Campos Principais de Login ---
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Nome', null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Sobrenome', null=True, blank=True)
    
    # --- Campos de Controle (Django) ---
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # --- Campos Novos (Perfil / Configurações) ---
    # Foto de upload (do computador)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    country = CountryField(blank=True)
    timezone = models.CharField(max_length=100, blank=True, default='UTC')

    # Em accounts/models.py (Dentro da classe CustomUser)

    # ... (Campos que você já tem: country, timezone, etc) ...

    # --- Campos de Notificações ---
    email_digest = models.BooleanField(default=True, verbose_name="Resumo Semanal")
    security_alerts = models.BooleanField(default=True, verbose_name="Alertas de Segurança")
    marketing_emails = models.BooleanField(default=False, verbose_name="E-mails de Marketing")
    
    # ... (Métodos __str__, get_full_name, etc) ...

    # --- Campos Legados (Google OAuth) ---
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # Mantemos este caso o login social salve a URL da foto aqui
    google_profile_picture = models.URLField(blank=True, null=True)

    # --- Conexão com o Gerente ---
    objects = CustomUserManager()

    # Configurações de Login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        # Retorna nome completo ou o email se não tiver nome
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email