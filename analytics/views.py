# Em analytics/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from . import youtube_service
import json
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


# --- [FUNÇÃO HELPER] ---
# (Colando ela aqui para garantir que ela exista)
def calculate_percentage_change(current, previous):
    if previous == 0:
        if current > 0:
            return 100.0 # Se saiu de 0 para >0, é 100% de aumento
        else:
            return 0.0 # Se era 0 e é 0, mudou 0%
    
    change = ((current - previous) / previous) * 100
    return round(change, 2) # Arredonda para 2 casas decimais
# ------------------------------


# --- [A VIEW INTEIRA E CORRIGIDA] ---
@login_required
def dashboard_view(request):
    
    context = {
        'error_message': None,
        'kpi_cards': {}, # Agora é um dict vazio
        'comparison_card': {}, # Novo card
        'insights_chart_data': None,
        'video_table_data': None,
        'region_chart_data': None,
    }

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile, created = Profile.objects.get_or_create(user=request.user)

    if not profile.youtube_channel_id:
        # (Lógica de erro do canal)
        logger.warning(f"Usuário {request.user.email} não tem youtube_channel_id no perfil.")
        context['error_message'] = (
            "Não foi possível encontrar um ID de canal do YouTube associado à sua conta Google. "
            "Por favor, faça logout e tente logar com uma conta Google que seja proprietária de um canal."
        )
        return render(request, 'analytics/index.html', context)
    
    
    # --- LÓGICA DE CACHE (Igual) ---
    cache_key = f"dashboard_data_{request.user.id}"
    dashboard_data = cache.get(cache_key)
    
    if not dashboard_data:
        logger.info(f"Cache miss para {cache_key}. Buscando dados frescos da API...")
        dashboard_data = youtube_service.get_dashboard_data(request.user)
        if not dashboard_data.get('error'):
            cache.set(cache_key, dashboard_data, timeout=10800) 
    else:
        logger.info(f"Cache hit para {cache_key}. Usando dados cacheados.")
        

    
    # --- [O 'TRY' QUE ESTAVA ABERTO] ---
    try:
        if dashboard_data.get('error'):
            context['error_message'] = dashboard_data['error']
            return render(request, 'analytics/index.html', context)

        # --- a) Processa os KPIs (Atual vs. Anterior) ---
        def get_kpi_totals(data_block):
            totals = {}
            if not data_block.get('rows'): 
                return {'views': 0, 'likes': 0, 'comments': 0, 'shares': 0, 'subscribers_net': 0}

            headers = {h['name']: i for i, h in enumerate(data_block.get('columnHeaders', []))}
            row = data_block['rows'][0]
            
            totals['views'] = row[headers.get('views', 0)]
            totals['likes'] = row[headers.get('likes', 0)]
            totals['comments'] = row[headers.get('comments', 0)]
            totals['shares'] = row[headers.get('shares', 0)]
            gained = row[headers.get('subscribersGained', 0)]
            lost = row[headers.get('subscribersLost', 0)]
            totals['subscribers_net'] = gained - lost
            
            return totals

        current_totals = get_kpi_totals(dashboard_data.get('kpi_current_period', {}))
        previous_totals = get_kpi_totals(dashboard_data.get('kpi_previous_period', {}))

        context['kpi_cards'] = {
            'views': current_totals['views'],
            'views_change': calculate_percentage_change(current_totals['views'], previous_totals['views']),
            'likes': current_totals['likes'],
            'likes_change': calculate_percentage_change(current_totals['likes'], previous_totals['likes']),
            'subscribers': current_totals['subscribers_net'],
            'subscribers_change': calculate_percentage_change(current_totals['subscribers_net'], previous_totals['subscribers_net']),
        }
        
        # --- (Onde o seu erro aconteceu) ---
        context['comparison_card'] = {
            'views': current_totals['views'],           # <-- [LINHA NOVA]
            'views_prev': previous_totals['views'],       # <-- [LINHA NOVA]
            'views_change': context['kpi_cards']['views_change'], # <-- [LINHA NOVA]
            'likes': current_totals['likes'],
            'likes_prev': previous_totals['likes'], 
            'likes_change': context['kpi_cards']['likes_change'],
            'comments': current_totals['comments'],
            'comments_prev': previous_totals['comments'], 
            'comments_change': calculate_percentage_change(current_totals['comments'], previous_totals['comments']),
            'shares': current_totals['shares'],
            'shares_prev': previous_totals['shares'], 
            'shares_change': calculate_percentage_change(current_totals['shares'], previous_totals['shares']),
        }

        # --- b) Processa o Gráfico de Insights ---
        analytics_data = dashboard_data.get('analytics_timeseries', {})
        analytics_rows = analytics_data.get('rows', [])
        analytics_headers = analytics_data.get('columnHeaders', []) 
        
        if analytics_rows and analytics_headers:
            header_map = {h['name']: i for i, h in enumerate(analytics_headers)}
            idx_day = header_map.get('day')
            idx_views = header_map.get('views')
            idx_likes = header_map.get('likes')

            if all([idx_day is not None, idx_views is not None, idx_likes is not None]):
                chart_labels = [row[idx_day] for row in analytics_rows]
                chart_views = [row[idx_views] for row in analytics_rows]
                chart_likes = [row[idx_likes] for row in analytics_rows]
                
                insights_data = {
                    'labels': chart_labels,
                    'datasets': [
                        { 'label': 'Visualizações', 'data': chart_views, 'backgroundColor': '#9D4EDD' },
                        { 'label': 'Likes', 'data': chart_likes, 'backgroundColor': '#E845A0' },
                    ]
                }
                context['insights_chart_data'] = json.dumps(insights_data)
        
        # --- c) Processa o Gráfico de Região ---
        region_rows = dashboard_data.get('region_data', {}).get('rows', [])
        if region_rows:
            region_labels = [row[0] for row in region_rows] 
            region_views = [row[1] for row in region_rows]
            region_data = {
                'labels': region_labels,
                'datasets': [{
                    'label': 'Visualizações por Região',
                    'data': region_views,
                    'backgroundColor': ['#9D4EDD', '#E845A0', '#00C49F', '#FFBB28', '#FF8042'],
                    'hoverOffset': 4
                }]
            }
            context['region_chart_data'] = json.dumps(region_data)

        # --- d) Processa a Tabela de Vídeos ---
        video_stats_list = dashboard_data.get('video_list_stats', [])
        table_rows = []
        for video in video_stats_list:
            table_rows.append({
                'title': video['snippet']['title'],
                'thumbnail': video['snippet']['thumbnails']['default']['url'],
                'status': 'Ativo',
                'likes': int(video['statistics'].get('likeCount', 0)),
                'comments': int(video['statistics'].get('commentCount', 0)),
            })
        context['video_table_data'] = table_rows
            
    # --- [O BLOCO QUE FALTAVA!] ---
    except Exception as e:
        logger.exception(f"Erro fatal ao processar dados na dashboard_view: {e}")
        context['error_message'] = f"Um erro inesperado ao processar dados: {e}"

    return render(request, 'analytics/index.html', context)