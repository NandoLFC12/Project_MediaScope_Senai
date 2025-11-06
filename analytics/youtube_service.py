# Em analytics/youtube_service.py
import logging
from datetime import datetime, timedelta

# Libs do Google
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Libs do Social Auth para pegar/atualizar o token
from social_django.utils import load_strategy

logger = logging.getLogger(__name__)

# Em analytics/youtube_service.py

def get_user_credentials(user):
    """
    Pega o 'social_auth' do usuário, usa a função INTELIGENTE 
    get_access_token() para pegar um token válido (renovando se necessário).
    """
    try:
        # 1. Carrega o 'strategy' (necessário para o get_access_token)
        strategy = load_strategy()

        # 2. Pega o 'social_auth' do usuário
        social = user.social_auth.get(provider='google-oauth2')

        # 3. USA A FUNÇÃO INTELIGENTE DA BIBLIOTECA
        # Ela vai automaticamente usar o refresh_token se o access_token tiver expirado
        access_token = social.get_access_token(strategy)

        if not access_token:
            # Isso acontece se o refresh_token falhar ou estiver ausente
            raise Exception("Não foi possível obter um access_token (pode estar faltando o refresh_token).")

        # 4. Retorna as credenciais prontas
        return Credentials(token=access_token)

    except Exception as e:
        # O erro 'e' agora será mais descritivo
        logger.error(f"Erro ao pegar/atualizar credenciais do usuário {user.email}: {e}")
        return None

# --- 2. O CONSTRUTOR DE SERVIÇOS ---
# Esta função usa as credenciais para criar os "serviços" de API
def build_youtube_services(credentials):
    """
    Recebe as credenciais e retorna os serviços de API
    prontos para fazer chamadas.
    """
    if not credentials:
        return None, None
        
    try:
        # Serviço para a API de DADOS (buscar vídeos, contagens públicas)
        youtube_data_service = build('youtube', 'v3', credentials=credentials)
        
        # Serviço para a API de ANALYTICS (buscar impressões, dados privados)
        youtube_analytics_service = build('youtubeAnalytics', 'v2', credentials=credentials)
        
        return youtube_data_service, youtube_analytics_service
        
    except HttpError as e:
        logger.error(f"Erro ao construir serviços do YouTube: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Erro desconhecido ao construir serviços: {e}")
        return None, None


# Em analytics/youtube_service.py

# ... (todos os imports e as funções get_user_credentials, build_youtube_services
#      continuam IGUAIS aqui em cima) ...


# Em analytics/youtube_service.py

# ... (imports e funções get_user_credentials, build_youtube_services
#      permanecem os mesmos) ...

# Em analytics/youtube_service.py

# ... (imports e funções get_user_credentials, build_youtube_services
#      permanecem os mesmos) ...

def get_dashboard_data(user):
    
    if not user.profile.youtube_channel_id:
        return {'error': 'ID do Canal não encontrado no perfil.'}
    
    channel_id = user.profile.youtube_channel_id
    
    credentials = get_user_credentials(user)
    if not credentials:
        return {'error': 'Falha ao autenticar com o Google. Tente fazer login novamente.'}
        
    youtube, youtube_analytics = build_youtube_services(credentials)
    if not youtube or not youtube_analytics:
        return {'error': 'Falha ao iniciar os serviços da API do YouTube.'}

    # --- 1. DEFINIÇÃO DE DATAS (ATUAL E ANTERIOR) ---
    
    # Período Atual (últimos 28 dias, com buffer de 2 dias)
    end_date_current = datetime.now().date() - timedelta(days=2)
    start_date_current = end_date_current - timedelta(days=27) 
    start_date_current_str = start_date_current.strftime('%Y-%m-%d')
    end_date_current_str = end_date_current.strftime('%Y-%m-%d')
    
    # Período Anterior (os 28 dias antes do período atual)
    end_date_previous = start_date_current - timedelta(days=1)
    start_date_previous = end_date_previous - timedelta(days=27)
    start_date_previous_str = start_date_previous.strftime('%Y-%m-%d')
    end_date_previous_str = end_date_previous.strftime('%Y-%m-%d')

    data = {}
    
    # Métricas que queremos para os KPIs (imagem original)
    kpi_metrics = "views,likes,comments,shares,subscribersGained,subscribersLost"

    try:
        # --- 2. CHAMADAS DE API ---
        
        # CHAMADA A: Gráfico de Insights (Dados por dia, período ATUAL)
        analytics_request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date_current_str,
            endDate=end_date_current_str,
            metrics="views,likes", # Gráfico só precisa desses dois
            dimensions="day",
            sort="day"
        )
        analytics_response = analytics_request.execute()
        data['analytics_timeseries'] = analytics_response

        # CHAMADA B: KPIs (Totais, período ATUAL)
        kpi_current_request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date_current_str,
            endDate=end_date_current_str,
            metrics=kpi_metrics # Pede views, likes, comments, shares, subs
            # (Sem 'dimensions', a API retorna os totais)
        )
        kpi_current_response = kpi_current_request.execute()
        data['kpi_current_period'] = kpi_current_response

        # CHAMADA C: KPIs (Totais, período ANTERIOR)
        kpi_previous_request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date_previous_str,
            endDate=end_date_previous_str,
            metrics=kpi_metrics # Pede as mesmas métricas, do período anterior
        )
        kpi_previous_response = kpi_previous_request.execute()
        data['kpi_previous_period'] = kpi_previous_response

        # CHAMADA D: Gráfico de Região (Período ATUAL)
        region_request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date_current_str,
            endDate=end_date_current_str,
            metrics="views",
            dimensions="country",
            sort="-views",
            maxResults=5
        )
        region_response = region_request.execute()
        data['region_data'] = region_response

        # CHAMADA E: Lista de Vídeos (Já estava correta)
        channel_request = youtube.channels().list(
            part="contentDetails", id=channel_id
        )
        channel_response = channel_request.execute()
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos_request = youtube.playlistItems().list(
            part="snippet", playlistId=uploads_playlist_id, maxResults=5
        )
        videos_response = videos_request.execute()
        video_items = videos_response.get('items', [])
        video_ids = [item['snippet']['resourceId']['videoId'] for item in video_items]

        if video_ids:
            stats_request = youtube.videos().list(
                part="snippet,statistics", id=",".join(video_ids)
            )
            stats_response = stats_request.execute()
            data['video_list_stats'] = stats_response.get('items', [])
        else:
            data['video_list_stats'] = []

        return data

    except HttpError as e:
        logger.error(f"HttpError ao buscar dados do dashboard: {e}")
        return {'error': f"Erro na API do YouTube: {e}. Verifique suas permissões."}
    except Exception as e:
        logger.error(f"Erro geral ao buscar dados do dashboard: {e}")
        return {'error': f"Erro inesperado: {e}"}