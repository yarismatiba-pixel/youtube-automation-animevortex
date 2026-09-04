"""
Main Script - Automatisation YouTube AnimeVortex
Menu principal pour utiliser tous les outils d'automatisation
"""

import os
import sys
from dotenv import load_dotenv
from youtube_uploader import YouTubeUploader
from youtube_playlists import YouTubePlaylistManager
from youtube_stats import YouTubeStats
from youtube_editor import YouTubeVideoEditor

load_dotenv()

class YouTubeAutomationMenu:
    def __init__(self):
        self.uploader = YouTubeUploader()
        self.playlist_manager = YouTubePlaylistManager()
        self.stats = YouTubeStats()
        self.editor = YouTubeVideoEditor()
    
    def display_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*60)
        print("🎬 YOUTUBE AUTOMATION - ANIMEVORTEX")
        print("="*60)
        print("\n1. 📹 Upload une vidéo")
        print("2. 📂 Upload plusieurs vidéos")
        print("3. 📋 Gérer les playlists")
        print("4. 📊 Voir les statistiques")
        print("5. ✏️  Modifier les vidéos")
        print("6. ⚙️  Configuration")
        print("0. ❌ Quitter")
        print("\n" + "="*60)
    
    def upload_single_video(self):
        """Upload une seule vidéo"""
        print("\n📹 UPLOAD UNE VIDÉO")
        print("-" * 40)
        
        video_path = input("Chemin du fichier vidéo: ").strip()
        title = input("Titre de la vidéo: ").strip()
        description = input("Description (optionnel, appuyez sur Entrée pour défaut): ").strip()
        tags_input = input("Tags séparés par des virgules (ex: anime,action): ").strip()
        thumbnail_path = input("Chemin de la miniature (optionnel): ").strip()
        is_public = input("Publier maintenant? (o/n): ").lower() == 'o'
        
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        thumbnail = thumbnail_path if thumbnail_path else None
        
        try:
            result = self.uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description if description else None,
                tags=tags if tags else None,
                thumbnail_path=thumbnail,
                is_public=is_public
            )
            print("\n✅ Vidéo uploadée avec succès!")
            print(f"URL: {result['url']}")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    
    def upload_batch_videos(self):
        """Upload plusieurs vidéos"""
        print("\n📂 UPLOAD PLUSIEURS VIDÉOS")
        print("-" * 40)
        
        json_file = input("Chemin du fichier JSON avec les vidéos: ").strip()
        
        if not os.path.exists(json_file):
            print(f"❌ Fichier {json_file} introuvable")
            return
        
        import json
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                videos_list = json.load(f)
            
            results = self.uploader.batch_upload(videos_list)
            
            print("\n" + "="*60)
            print("📊 RÉSUMÉ DES UPLOADS")
            print("="*60)
            print(f"Total: {len(results)}")
            print(f"Succès: {sum(1 for r in results if 'video_id' in r)}")
            print(f"Erreurs: {sum(1 for r in results if 'error' in r)}")
            print("="*60)
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def manage_playlists(self):
        """Gère les playlists"""
        print("\n📋 GESTION DES PLAYLISTS")
        print("-" * 40)
        print("1. Voir mes playlists")
        print("2. Créer une nouvelle playlist")
        print("3. Ajouter des vidéos à une playlist")
        print("0. Retour")
        
        choice = input("\nChoix: ").strip()
        
        if choice == '1':
            self.playlist_manager.display_playlists()
        elif choice == '2':
            title = input("Titre de la playlist: ").strip()
            description = input("Description: ").strip()
            is_public = input("Public? (o/n): ").lower() == 'o'
            self.playlist_manager.create_playlist(title, description, is_public)
        elif choice == '3':
            playlist_id = input("ID de la playlist: ").strip()
            video_ids_input = input("IDs des vidéos (séparés par des virgules): ").strip()
            video_ids = [vid.strip() for vid in video_ids_input.split(',')]
            self.playlist_manager.add_videos_to_playlist(playlist_id, video_ids)
    
    def view_statistics(self):
        """Affiche les statistiques"""
        print("\n📊 STATISTIQUES")
        print("-" * 40)
        print("1. Stats de la chaîne")
        print("2. Stats des vidéos récentes")
        print("3. Top vidéos (par vues)")
        print("0. Retour")
        
        choice = input("\nChoix: ").strip()
        
        if choice == '1':
            self.stats.get_channel_stats_formatted()
        elif choice == '2':
            limit = input("Nombre de vidéos (défaut 10): ").strip()
            limit = int(limit) if limit else 10
            self.stats.display_recent_videos_stats(limit)
        elif choice == '3':
            limit = input("Nombre de vidéos (défaut 10): ").strip()
            limit = int(limit) if limit else 10
            self.stats.display_top_videos(limit)
    
    def edit_videos(self):
        """Modifie les vidéos"""
        print("\n✏️  ÉDITION DES VIDÉOS")
        print("-" * 40)
        print("1. Modifier le titre")
        print("2. Modifier la description")
        print("3. Modifier les tags")
        print("4. Ajouter un footer à la description")
        print("0. Retour")
        
        choice = input("\nChoix: ").strip()
        video_id = input("ID de la vidéo: ").strip()
        
        if choice == '1':
            new_title = input("Nouveau titre: ").strip()
            self.editor.update_video_title(video_id, new_title)
        elif choice == '2':
            new_desc = input("Nouvelle description: ").strip()
            self.editor.update_video_description(video_id, new_desc)
        elif choice == '3':
            tags_input = input("Nouveaux tags (séparés par des virgules): ").strip()
            tags = [tag.strip() for tag in tags_input.split(',')]
            self.editor.update_video_tags(video_id, tags)
        elif choice == '4':
            footer = input("Footer à ajouter: ").strip()
            self.editor.add_description_footer(video_id, footer)
    
    def show_configuration(self):
        """Affiche la configuration"""
        print("\n⚙️  CONFIGURATION")
        print("-" * 40)
        print(f"Channel ID: {os.getenv('CHANNEL_ID', 'Non défini')}")
        print(f"Channel Name: {os.getenv('CHANNEL_NAME', 'Non défini')}")
        print(f"Catégorie par défaut: {os.getenv('DEFAULT_CATEGORY_ID', '24')}")
        print(f"Langue: {os.getenv('DEFAULT_LANGUAGE', 'fr')}")
        print("\n✏️  Éditez le fichier .env pour modifier la configuration")
    
    def run(self):
        """Lance le menu principal"""
        while True:
            self.display_menu()
            choice = input("Votre choix: ").strip()
            
            if choice == '1':
                self.upload_single_video()
            elif choice == '2':
                self.upload_batch_videos()
            elif choice == '3':
                self.manage_playlists()
            elif choice == '4':
                self.view_statistics()
            elif choice == '5':
                self.edit_videos()
            elif choice == '6':
                self.show_configuration()
            elif choice == '0':
                print("\n👋 Au revoir!")
                break
            else:
                print("❌ Choix invalide")

if __name__ == '__main__':
    try:
        menu = YouTubeAutomationMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
