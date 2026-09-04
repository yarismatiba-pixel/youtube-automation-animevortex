"""
YouTube Video Editor Module
Modifier les titres, descriptions et autres infos des vidéos
"""

import os
from youtube_auth import get_youtube_service

class YouTubeVideoEditor:
    def __init__(self):
        self.youtube = get_youtube_service()
    
    def update_video_description(self, video_id, new_description):
        """
        Met à jour la description d'une vidéo
        """
        try:
            # Récupère la vidéo actuelle
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                video['snippet']['description'] = new_description
                
                # Met à jour
                self.youtube.videos().update(
                    part='snippet',
                    body=video
                ).execute()
                
                print(f"✅ Description mise à jour pour {video_id}")
                return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    def update_video_title(self, video_id, new_title):
        """
        Met à jour le titre d'une vidéo
        """
        try:
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                video['snippet']['title'] = new_title
                
                self.youtube.videos().update(
                    part='snippet',
                    body=video
                ).execute()
                
                print(f"✅ Titre mis à jour pour {video_id}")
                return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    def update_video_tags(self, video_id, new_tags):
        """
        Met à jour les tags d'une vidéo
        """
        try:
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                video['snippet']['tags'] = new_tags
                
                self.youtube.videos().update(
                    part='snippet',
                    body=video
                ).execute()
                
                print(f"✅ Tags mis à jour pour {video_id}")
                return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    def batch_update_descriptions(self, updates_list):
        """
        Met à jour les descriptions de plusieurs vidéos
        
        Args:
            updates_list: Liste de dicts avec 'video_id' et 'description'
        """
        results = []
        for i, update in enumerate(updates_list, 1):
            print(f"\n[{i}/{len(updates_list)}] Mise à jour de {update['video_id']}")
            result = self.update_video_description(
                update['video_id'],
                update['description']
            )
            results.append({
                'video_id': update['video_id'],
                'success': result
            })
        
        print(f"\n✅ {sum(1 for r in results if r['success'])}/{len(results)} descriptions mises à jour")
        return results
    
    def add_description_footer(self, video_id, footer_text):
        """
        Ajoute du texte à la fin de la description existante
        """
        try:
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                current_desc = video['snippet']['description']
                video['snippet']['description'] = current_desc + '\n\n' + footer_text
                
                self.youtube.videos().update(
                    part='snippet',
                    body=video
                ).execute()
                
                print(f"✅ Footer ajouté à {video_id}")
                return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
