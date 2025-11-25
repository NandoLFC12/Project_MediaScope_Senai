from django.core.management.base import BaseCommand
from subscriptions.models import Plan

class Command(BaseCommand):
    help = 'Cria os planos iniciais do sistema automaticamente'

    def handle(self, *args, **kwargs):
        # Configuração dos Planos (Baseado nos campos do seu Model)
        plans_data = [
            {
                'name': 'Essential',
                'price_monthly': 299.00,
                'price_annual': 268.00,
                'icon_name': 'workspace_premium',  
            },
            {
                'name': 'Professional',
                'price_monthly': 599.00,
                'price_annual': 541.00, 
                'icon_name': 'auto_awesome',
            },
            {
                'name': 'Enterprise',
                'price_monthly': 1299.00,
                'price_annual': 1269.00,
                'icon_name': 'domain',
            }
        ]

        self.stdout.write('Iniciando a criação dos planos...')

        for data in plans_data:
            # O get_or_create busca pelo 'name' e cria se não achar
            plan, created = Plan.objects.get_or_create(
                name=data['name'],
                defaults={
                    'price_monthly': data['price_monthly'],
                    'price_annual': data['price_annual'],
                    'icon_name': data['icon_name'],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Plan "{plan.name}" criado com sucesso!'))
            else:
                # Se o plano já existe, vamos atualizar os preços para garantir
                plan.price_monthly = data['price_monthly']
                plan.price_annual = data['price_annual']
                plan.icon_name = data['icon_name']
                plan.save()
                self.stdout.write(self.style.WARNING(f'🔄 Plan "{plan.name}" atualizado.'))

        self.stdout.write(self.style.SUCCESS('--- Configuração de Planos Concluída! ---'))