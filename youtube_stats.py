"""
YouTube Statistics Module
Récupère et affiche les stats de la chaîne et des vidéos
"""

import os
from youtube_auth import get_youtube_service
from datetime import datetime

class YouTubeStats:
    def __init__(self):
        self.youtube = get_youtube_service()
        self.channel_id = os.getenv('CHANNEL_ID')
    
    def get_channel_stats(self):
        """
        Récupère les stats globales de la chaîne
        """
        request = self.youtube.channels().list(
            part='statistics,snippet',
            id=self.channel_id
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]
            stats = channel['statistics']
            snippet = channel['snippet']
            
            return {
                'channel_name': snippet['title'],
                'description': snippet['description'],
                'view_count': int(stats.get('viewCount', 0)),
                'subscriber_count': int(stats.get('subscriberCount', 0)),
                'video_count': int(stats.get('videoCount', 0)),
                'uploads_playlist_id': channel['contentDetails']['relatedPlaylists']['uploads']
            }
        return None
    
    def get_channel_stats_formatted(self):
        """
        Affiche les stats de la chaîne de manière lisible
        """
        stats = self.get_channel_stats()
        if not stats:
            return "Chaîne non trouvée"
        
        print("\n" + "="*50)
        print(f"📺 Chaîne: {stats['channel_name']}")
        print("="*50)
        print(f"👥 Abonnés: {stats['subscriber_count']:,}")
        print(f"👁️  Vues totales: {stats['view_count']:,}")
        print(f"🎬 Nombre de vidéos: {stats['video_count']}")
        print("="*50 + "\n")
        
        return stats
    
    def get_video_stats(self, video_id):
        """
        Récupère les stats d'une vidéo spécifique
        """
        request = self.youtube.videos().list(
            part='statistics,snippet,contentDetails',
            id=video_id
        )
        response = request.execute()
        
        if response['items']:
            video = response['items'][0]
            stats = video['statistics']
            snippet = video['snippet']
            
            return {
                'video_id': video_id,
                'title': snippet['title'],
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'published_at': snippet['publishedAt'],
                'duration': video['contentDetails']['duration']
            }
        return None
    
    def get_recent_videos(self, max_results=10):
        """
        Récupère les vidéos récentes
        """
        stats = self.get_channel_stats()
        uploads_playlist_id = stats['uploads_playlist_id']
        
        request = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=max_results,
            order='date'
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_stats = self.get_video_stats(video_id)
            videos.append(video_stats)
        
        return videos
    
    def display_recent_videos_stats(self, max_results=10):
        """
        Affiche les stats des vidéos récentes de manière lisible
        """
        videos = self.get_recent_videos(max_results)
        
        print("\n" + "="*80)
        print(f"📊 STATS DES {len(videos)} DERNIÈRES VIDÉOS")
        print("="*80)
        
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. {video['title']}")
            print(f"   ID: {video['video_id']}")
            print(f"   👁️  Vues: {video['view_count']:,}")
            print(f"   👍 Likes: {video['like_count']:,}")
            print(f"   💬 Commentaires: {video['comment_count']:,}")
            print(f"   📅 Publié: {video['published_at'][:10]}")
        
        print("\n" + "="*80 + "\n")
        
        return videos
    
    def get_top_videos(self, max_results=10):
        """
        Récupère les vidéos les plus regardées
        """
        videos = self.get_recent_videos(max_results * 2)
        sorted_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)
        return sorted_videos[:max_results]
    
    def display_top_videos(self, max_results=10):
        """
        Affiche les vidéos les plus regardées
        """
        videos = self.get_top_videos(max_results)
        
        print("\n" + "="*80)
        print(f"🏆 TOP {len(videos)} VIDÉOS (par vues)")
        print("="*80)
        
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. {video['title']}")
            print(f"   👁️  Vues: {video['view_count']:,}")
            print(f"   👍 Likes: {video['like_count']:,}")
            print(f"   💬 Commentaires: {video['comment_count']:,}")
        
        print("\n" + "="*80 + "\n")
        
        return videos
