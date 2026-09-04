"""
YouTube Playlists Management Module
Créer, modifier et gérer les playlists
"""

import os
from youtube_auth import get_youtube_service

class YouTubePlaylistManager:
    def __init__(self):
        self.youtube = get_youtube_service()
        self.channel_id = os.getenv('CHANNEL_ID')
    
    def create_playlist(self, title, description='', is_public=True):
        """
        Crée une nouvelle playlist
        
        Args:
            title: Titre de la playlist
            description: Description de la playlist
            is_public: Public ou privée
        
        Returns:
            dict: Infos de la playlist créée
        """
        body = {
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'public' if is_public else 'private'
            }
        }
        
        request = self.youtube.playlists().insert(
            part='snippet,status',
            body=body
        )
        response = request.execute()
        
        playlist_id = response['id']
        print(f"✅ Playlist créée: {title}")
        print(f"   ID: {playlist_id}")
        
        return {
            'playlist_id': playlist_id,
            'title': title,
            'url': f'https://www.youtube.com/playlist?list={playlist_id}'
        }
    
    def get_playlists(self):
        """
        Récupère toutes les playlists de la chaîne
        """
        request = self.youtube.playlists().list(
            part='snippet',
            channelId=self.channel_id,
            maxResults=50
        )
        response = request.execute()
        
        playlists = []
        for item in response['items']:
            playlists.append({
                'playlist_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt']
            })
        
        return playlists
    
    def display_playlists(self):
        """
        Affiche les playlists de manière lisible
        """
        playlists = self.get_playlists()
        
        print("\n" + "="*60)
        print("📋 MES PLAYLISTS")
        print("="*60)
        
        for i, playlist in enumerate(playlists, 1):
            print(f"\n{i}. {playlist['title']}")
            print(f"   ID: {playlist['playlist_id']}")
            print(f"   Description: {playlist['description'][:50]}...")
        
        print("\n" + "="*60 + "\n")
        
        return playlists
    
    def add_videos_to_playlist(self, playlist_id, video_ids):
        """
        Ajoute plusieurs vidéos à une playlist
        
        Args:
            playlist_id: ID de la playlist
            video_ids: Liste d'IDs de vidéos
        """
        added = 0
        for video_id in video_ids:
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            try:
                self.youtube.playlistItems().insert(
                    part='snippet',
                    body=body
                ).execute()
                added += 1
                print(f"✅ Vidéo {video_id} ajoutée")
            except Exception as e:
                print(f"❌ Erreur pour {video_id}: {e}")
        
        print(f"\n✅ {added}/{len(video_ids)} vidéos ajoutées à la playlist")
    
    def get_playlist_videos(self, playlist_id, max_results=50):
        """
        Récupère les vidéos d'une playlist
        """
        request = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            videos.append({
                'video_id': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title'],
                'position': item['snippet']['position']
            })
        
        return videos
    
    def delete_playlist(self, playlist_id):
        """
        Supprime une playlist
        """
        try:
            self.youtube.playlists().delete(id=playlist_id).execute()
            print(f"✅ Playlist {playlist_id} supprimée")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            return False
    
    def update_playlist_description(self, playlist_id, description):
        """
        Met à jour la description d'une playlist
        """
        try:
            # D'abord récupère la playlist actuelle
            request = self.youtube.playlists().list(
                part='snippet,status',
                id=playlist_id
            )
            response = request.execute()
            
            if response['items']:
                playlist = response['items'][0]
                playlist['snippet']['description'] = description
                
                # Met à jour
                self.youtube.playlists().update(
                    part='snippet,status',
                    body=playlist
                ).execute()
                
                print(f"✅ Description de la playlist mise à jour")
                return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
