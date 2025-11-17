# Em accounts/pipeline.py

import logging
import requests
from django.core.files.base import ContentFile
from analytics.models import Profile
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

def save_youtube_channel_data(backend, user, response, *args, **kwargs):
    """
    Busca os dados do CANAL do YouTube:
    1. O ID do canal (para estatísticas).
    2. A Foto do canal (para o perfil), se o usuário não tiver uma.
    """
    
    # Cria ou pega o perfil
    profile, created = Profile.objects.get_or_create(user=user)

    # Precisamos do token para falar com o YouTube
    access_token = response.get('access_token')
    if not access_token:
        return

    try:
        # Conecta na API do YouTube
        credentials = Credentials(token=access_token)
        youtube_service = build('youtube', 'v3', credentials=credentials)
        
        # --- O PULO DO GATO ---
        # Pedimos 'id' E 'snippet' (o snippet contém a foto e o título)
        request = youtube_service.channels().list(
            part="id,snippet", 
            mine=True
        )
        api_response = request.execute()

        if api_response.get('items'):
            item = api_response['items'][0]
            
            # 1. SALVAR O ID DO CANAL (Vital para o Dashboard)
            channel_id = item['id']
            if profile.youtube_channel_id != channel_id:
                profile.youtube_channel_id = channel_id
                profile.save()
                logger.info(f"ID do canal salvo: {channel_id}")

            # 2. SALVAR A FOTO DO CANAL (Se o usuário não tiver foto)
            if not user.profile_picture:
                # Pega a URL da foto de alta qualidade do canal
                thumbnails = item['snippet']['thumbnails']
                # Tenta pegar a maior possível: high > medium > default
                picture_url = thumbnails.get('high', thumbnails.get('medium', thumbnails.get('default')))['url']
                
                if picture_url:
                    image_response = requests.get(picture_url)
                    if image_response.status_code == 200:
                        user.profile_picture.save(
                            f"youtube_avatar_{user.id}.jpg", 
                            ContentFile(image_response.content), 
                            save=True
                        )
                        logger.info(f"Foto do Canal YouTube salva para {user.email}")

    except Exception as e:
        logger.error(f"Erro ao buscar dados do YouTube: {e}")