# Em accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm # <--- ADICIONE SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from .forms import SignUpForm, SignInForm, ProfileForm, NotificationForm
from .models import CustomUser

class AuthView(View):
    """
    View principal que gerencia login e registro
    """
    def get(self, request):
        # Se já estiver logado, redireciona para dashboard
        if request.user.is_authenticated:
            # [CONSERTO 1: O NOME DA URL MUDOU]
            return redirect('dashboard_home') 
        
        signup_form = SignUpForm()
        signin_form = SignInForm()
        
        context = {
            'signup_form': signup_form,
            'signin_form': signin_form,
        }
        return render(request, 'accounts/auth.html', context)
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'signup':
            return self.handle_signup(request)
        elif action == 'signin':
            return self.handle_signin(request)
        
        # [CONSERTO 2: O NOME DA URL MUDOU]
        return redirect('login')
    
    def handle_signup(self, request):
        """
        Processa o registro de novo usuário
        """
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Cria o usuário (senha já é criptografada automaticamente)
            user = form.save()
            
            # Faz login automático após registro
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Mensagem de sucesso
            messages.success(
                request, 
                f'Bem-vindo, {user.get_full_name()}! Sua conta foi criada com sucesso.'
            )
            return redirect('dashboard_home') # <-- Este já estava certo!
        else:
            # Mostra erros de validação
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            
            signin_form = SignInForm()
            context = {
                'signup_form': form,
                'signin_form': signin_form,
                'active_tab': 'signup'
            }
            return render(request, 'accounts/auth.html', context)
    
    # Em accounts/views.py -> handle_signin

    def handle_signin(self, request):
    # Tenta pegar 'username', se não achar, tenta pegar 'email'
        email = request.POST.get('username') or request.POST.get('email') 
        password = request.POST.get('password')
    
    # ... resto do código igual
        
        # Autentica o usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Login bem-sucedido
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.get_full_name()}!')
            return redirect('dashboard_home') # <-- Este também já estava certo!
        else:
            # Credenciais inválidas
            messages.error(request, 'Email ou senha incorretos. Tente novamente.')
            
            signup_form = SignUpForm()
            signin_form = SignInForm()
            context = {
                'signup_form': signup_form,
                'signin_form': signin_form,
                'active_tab': 'signin'
            }
            return render(request, 'accounts/auth.html', context)

# Em accounts/views.py

@login_required
def settings_view(request):
    user = request.user
    active_tab = 'profile'
    
    # 1. Lógica Inteligente de Senha (Define qual formulário usar)
    if user.has_usable_password():
        PasswordFormClass = PasswordChangeForm
    else:
        PasswordFormClass = SetPasswordForm

    # 2. Inicializa os formulários (Padrão para GET)
    profile_form = ProfileForm(instance=user)
    notification_form = NotificationForm(instance=user)
    password_form = PasswordFormClass(user)
    
    google_connected = user.social_auth.filter(provider='google-oauth2').exists()

    # 3. Processamento do POST (Quando clica em Salvar)
    if request.method == 'POST':
        action = request.POST.get('action') # <--- action nasce aqui
        
        # --- AÇÃO 1: PERFIL ---
        if action == 'update_profile':
            active_tab = 'profile'
            profile_form = ProfileForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('settings')

       # --- AÇÃO 2: SENHA ---
        elif action == 'change_password':
            active_tab = 'security'
            password_form = PasswordFormClass(user, request.POST)
            
            if password_form.is_valid():
                user = password_form.save()
                
                # --- [A LINHA MÁGICA] ---
                # Isso mantém o usuário logado após mudar a senha
                update_session_auth_hash(request, user) 
                # ------------------------
                
                messages.success(request, 'Sua senha foi atualizada!')
                return redirect('settings')
            else:
                messages.error(request, 'Erro na senha. Verifique os campos.')

        # --- AÇÃO 3: NOTIFICAÇÕES ---
        elif action == 'update_notifications': # <--- GARANTA QUE ESTEJA DENTRO DO POST
            active_tab = 'notifications'
            notification_form = NotificationForm(request.POST, instance=user)
            if notification_form.is_valid():
                notification_form.save()
                messages.success(request, 'Preferências salvas!')
                return redirect('settings')

    # 4. Renderiza a página (GET ou POST com erro)
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'notification_form': notification_form,
        'google_connected': google_connected,
        'active_tab': active_tab,
        'has_password': user.has_usable_password()
    }
    return render(request, 'accounts/settings.html', context)

@login_required
def delete_account_view(request):
    """
    Zona de Perigo: Deleta o usuário e tudo relacionado a ele.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.info(request, 'Sua conta foi excluída permanentemente.')
        return redirect('login')
    
    # Se tentar acessar via GET, chuta de volta para settings
    return redirect('settings')

# Em accounts/views.py

@login_required
def disconnect_google_view(request):
    """
    Desconecta a conta do Google, mas apenas se o usuário tiver uma senha definida.
    """
    if request.method == 'POST':
        user = request.user
        
        # 1. Verifica se o usuário tem senha
        if not user.has_usable_password():
            messages.error(request, 'Para desconectar o Google, você primeiro precisa definir uma senha na aba "Segurança".')
            return redirect('settings')

        # 2. Tenta encontrar e apagar o vínculo
        try:
            google_account = user.social_auth.get(provider='google-oauth2')
            google_account.delete()
            messages.success(request, 'Conta do Google desconectada com sucesso.')
        except:
            messages.error(request, 'Nenhuma conta Google encontrada para desconectar.')
            
    return redirect('settings')