# Em accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django_countries.widgets import CountrySelectWidget

class SignUpForm(UserCreationForm):
    """
    Formulário de registro de novo usuário
    """
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
            'id': 'id_first_name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
            'id': 'id_last_name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'id': 'id_email'
        })
    )
    
    # (UserCreationForm já lida com senhas, mas se você sobrescreveu assim, ok)
    # password1 e password2...
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email') # Removi senhas daqui pq UserCreationForm processa separado
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado.')
        return email

class SignInForm(AuthenticationForm):
    """
    Formulário de login
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'id': 'signin-email'
        })
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'id': 'signin-password'
        })
    )

# --- AQUI ESTAVA O ERRO DE INDENTAÇÃO ---
# A classe ProfileForm deve começar na margem esquerda
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'country', 'timezone']
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-control form-select-dark'}), 
        }
        
    # O __init__ deve estar alinhado com a class Meta (dentro de ProfileForm)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Sobrenome'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['timezone'].widget.attrs.update({'class': 'form-control'})
        # self.fields['profile_picture']... (Django widget padrão já é ok, mas pode estilizar se quiser)

# --- A CLASSE NOVA ---
# Ela deve estar FORA do ProfileForm (na margem esquerda)
class NotificationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email_digest', 'security_alerts', 'marketing_emails']