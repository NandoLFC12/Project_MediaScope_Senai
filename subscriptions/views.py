# Em subscriptions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plan, Subscription, Payment
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages

@login_required
def planos_view(request):
    # Busca todos os planos do banco para mostrar na tela
    plans = Plan.objects.all().order_by('price_monthly')
    return render(request, 'analytics/planos.html', {'plans': plans})

@login_required
def upgrade_plan_view(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    user = request.user
    
    # 1. Descobre se é Anual ou Mensal (Vem pela URL: ?period=annual)
    period = request.GET.get('period', 'monthly')
    
    # 2. Calcula a data de vencimento
    if period == 'annual':
        days_to_add = 365
        amount = plan.price_annual
        cycle_name = "Anual"
    else:
        days_to_add = 30
        amount = plan.price_monthly
        cycle_name = "Mensal"

    # 3. Atualiza a Assinatura
    subscription, created = Subscription.objects.get_or_create(user=user)
    subscription.plan = plan
    subscription.status = 'active'
    
    # --- O PULO DO GATO: Define a data de renovação ---
    subscription.start_date = timezone.now()
    subscription.current_period_end = timezone.now() + timedelta(days=days_to_add)
    subscription.save()

    # 4. Gera o Pagamento Simulado
    if amount > 0:
        Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=amount
        )

    messages.success(request, f'Sucesso! Plano {plan.name} ({cycle_name}) assinado até {subscription.current_period_end.strftime("%d/%m/%Y")}.')
    return redirect('settings')
# Tranca a view: se o usuário não estiver logado,
# ele é enviado para a página 'home' (nosso login).
@login_required(login_url='home')
def subscribe_view(request, plan_id):
    """
    Simula a "compra" de um plano.
    """
    # 1. Pega o plano que o usuário clicou (ou dá erro 404)
    plan = get_object_or_404(Plan, id=plan_id)
    user = request.user

    # 2. Pega a assinatura do usuário (ou cria uma nova)
    # Isso é "de alto nível": impede que o usuário tenha 2 assinaturas
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        defaults={'plan': plan, 'status': Subscription.StatusChoices.ACTIVE}
    )

    # 3. Se a assinatura já existia (não foi 'created'),
    # apenas atualiza o plano e o status dela.
    if not created:
        subscription.plan = plan
        subscription.status = Subscription.StatusChoices.ACTIVE

    # 4. Define a data de "expiração" (daqui a 30 dias)
    subscription.current_period_end = datetime.now() + timedelta(days=30)
    subscription.save()

    # 5. CRIE O PAGAMENTO (O "KA-CHING!" 💰)
    # Isso é o que o seu Dashboard de Admin vai ler!
    Payment.objects.create(
        user=user,
        subscription=subscription,
        amount=plan.price_monthly # Ou o valor do plano
    )
    
    return redirect('dashboard_home')