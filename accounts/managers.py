# Em accounts/managers.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# NÃO IMPORTE 'CustomUser' AQUI! ISSO CRIA O LOOP.

class CustomUserManager(BaseUserManager):
    """
    Gerenciador para criar usuários via e-mail.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O e-mail deve ser definido'))
        email = self.normalize_email(email)
        
        # O truque: Usamos 'self.model' em vez de importar 'CustomUser'
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser precisa ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser precisa ter is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)