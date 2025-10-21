from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate


# ========================
# CONFIGURAÇÃO DA API
# ========================
API_KEY = 'AIzaSyBsyimLy3Y1V6lsg471XpyIEB9qGIsOsBA'
youtube = build('youtube', 'v3', developerKey=API_KEY)


# ========================
# FUNÇÃO 1 — VÍDEO
# ========================
def get_video_info(video_link: str) -> pd.DataFrame:
    """Coleta dados de um vídeo específico do YouTube"""
    if "v=" in video_link:
        video_id = video_link.split("v=")[1].split("&")[0]
    else:
        raise ValueError("Link inválido! Cole um link de vídeo do YouTube.")

    res = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    if not res["items"]:
        raise ValueError("Vídeo não encontrado ou é privado!")

    info = res["items"][0]
    snippet = info["snippet"]
    stats = info.get("statistics", {})

    data = {
        "video_id": [video_id],
        "title": [snippet["title"]],
        "description": [snippet.get("description", "")],
        "published_date": [snippet["publishedAt"]],
        "extraction_date": [str(datetime.now())],
        "thumbnail_url": [snippet["thumbnails"]["high"]["url"]],
        "likes": [int(stats.get("likeCount", 0))],
        "views": [int(stats.get("viewCount", 0))],
        "comments": [int(stats.get("commentCount", 0))]
    }

    df = pd.DataFrame(data)
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return df


# ========================
# FUNÇÃO 2 — PLAYLIST
# ========================
def get_playlist_info(playlist_link: str, playlist_name: str) -> pd.DataFrame:
    """Coleta dados de uma playlist do YouTube"""
    playlist_id = playlist_link.split("list=")[1].split("&")[0]
    next_page_token = None
    playlist_videos = []

    while True:
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        playlist_videos += res['items']
        next_page_token = res.get('nextPageToken')
        if not next_page_token:
            break

    print(f"🎞️ Total de vídeos na playlist '{playlist_name}': {len(playlist_videos)}")

    video_ids = [v['snippet']['resourceId']['videoId'] for v in playlist_videos]
    stats = []

    for vid in video_ids:
        s = youtube.videos().list(part='statistics', id=vid).execute()
        stats += s['items']

    # montar DataFrames
    meta_df = pd.DataFrame({
        "video_id": [v['snippet']['resourceId']['videoId'] for v in playlist_videos],
        "title": [v['snippet']['title'] for v in playlist_videos],
        "description": [v['snippet']['description'] for v in playlist_videos],
        "published_date": [v['snippet']['publishedAt'] for v in playlist_videos],
        "extraction_date": [str(datetime.now())]*len(video_ids),
        "url_thumbnails": [v['snippet']['thumbnails'] for v in playlist_videos]
    })

    stats_df = pd.DataFrame({
        "video_id": [v['id'] for v in stats],
        "liked": [int(v['statistics'].get('likeCount', 0)) for v in stats],
        "views": [int(v['statistics'].get('viewCount', 0)) for v in stats],
        "comment": [int(v['statistics'].get('commentCount', 0)) for v in stats],
    })

    playlist_df = pd.merge(meta_df, stats_df, on="video_id", how="left")
    print(tabulate(playlist_df.head(5), headers="keys", tablefmt="fancy_grid", showindex=False))
    return playlist_df


# ========================
# FUNÇÃO 3 — CANAL
# ========================
def get_channel_data(channel_link: str, save_files: bool = True):
    """Coleta dados de um canal e seus vídeos"""
    # --- Extrair ID ---
    if "/channel/" in channel_link:
        channel_id = channel_link.split("/channel/")[1].split("/")[0]
    elif "/@" in channel_link:
        username = channel_link.split("/@")[1].split("/")[0]
        res = youtube.channels().list(part="id", forHandle=username).execute()
        if not res["items"]:
            raise ValueError("Canal não encontrado!")
        channel_id = res["items"][0]["id"]
    else:
        raise ValueError("Link inválido! Use um link /channel/ ou /@nome")

    # --- Dados do canal ---
    res = youtube.channels().list(
        part="snippet,statistics,brandingSettings,contentDetails",
        id=channel_id
    ).execute()
    if not res["items"]:
        raise ValueError("Canal não encontrado ou é privado!")

    info = res["items"][0]
    snippet = info["snippet"]
    stats = info["statistics"]
    branding = info.get("brandingSettings", {})
    uploads_playlist_id = info["contentDetails"]["relatedPlaylists"]["uploads"]

    channel_df = pd.DataFrame({
        "channel_id": [channel_id],
        "title": [snippet["title"]],
        "description": [snippet.get("description", "")],
        "published_at": [snippet["publishedAt"]],
        "thumbnail": [snippet["thumbnails"]["high"]["url"]],
        "banner_url": [branding.get("image", {}).get("bannerExternalUrl", None)],
        "subscribers": [int(stats.get("subscriberCount", 0))],
        "total_views": [int(stats.get("viewCount", 0))],
        "total_videos": [int(stats.get("videoCount", 0))],
        "extraction_date": [str(datetime.now())]
    })

    print("\n✅ Dados gerais do canal:")
    print(tabulate(channel_df, headers="keys", tablefmt="fancy_grid", showindex=False))

    # --- Coleta dos vídeos ---
    print("\n📦 Coletando vídeos...")
    videos, next_page_token = [], None
    while True:
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        videos += res["items"]
        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break

    print(f"🔹 Total de vídeos: {len(videos)}")

    video_ids = [v["snippet"]["resourceId"]["videoId"] for v in videos]
    titles = [v["snippet"]["title"] for v in videos]
    dates = [v["snippet"]["publishedAt"] for v in videos]

    # --- Estatísticas ---
    all_stats = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        s = youtube.videos().list(part="statistics", id=",".join(batch)).execute()
        all_stats += s["items"]

    stats_dict = {v["id"]: v["statistics"] for v in all_stats}
    video_data = []
    for vid, title, date in zip(video_ids, titles, dates):
        s = stats_dict.get(vid, {})
        video_data.append({
            "video_id": vid,
            "title": title,
            "published_date": date,
            "views": int(s.get("viewCount", 0)),
            "likes": int(s.get("likeCount", 0)),
            "comments": int(s.get("commentCount", 0))
        })

    videos_df = pd.DataFrame(video_data)

    # --- Estatísticas gerais ---
    print("\n📊 Estatísticas agregadas:")
    print(f"➡️  Visualizações somadas: {videos_df['views'].sum():,}")
    print(f"👍  Total de likes: {videos_df['likes'].sum():,}")
    print(f"💬  Total de comentários: {videos_df['comments'].sum():,}")

    # --- Gráficos ---
    videos_df["published_date"] = pd.to_datetime(videos_df["published_date"])
    videos_df = videos_df.sort_values("published_date")

    plt.figure(figsize=(10, 5))
    plt.plot(videos_df["published_date"], videos_df["views"], marker="o")
    plt.title(f"Visualizações por vídeo - {channel_df['title'][0]}")
    plt.xlabel("Data")
    plt.ylabel("Views")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(videos_df["published_date"], videos_df["likes"], color="green", marker="o")
    plt.title(f"Likes por vídeo - {channel_df['title'][0]}")
    plt.xlabel("Data")
    plt.ylabel("Likes")
    plt.grid(True)
    plt.show()

    # --- Engajamento ---
    videos_df["engagement"] = (videos_df["likes"] / videos_df["views"] * 100).fillna(0)
    videos_df["url"] = "https://www.youtube.com/watch?v=" + videos_df["video_id"]

    if save_files:
        channel_df.to_csv("canal_info.csv", index=False)
        videos_df.to_csv("videos_info.csv", index=False)
        print("\n💾 Dados salvos em CSV!")

    return channel_df, videos_df
