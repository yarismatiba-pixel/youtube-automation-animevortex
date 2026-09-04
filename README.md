````markdown
# 🎬 YouTube Automation - AnimeVortex

Automatisez complètement votre chaîne YouTube avec Python et l'API YouTube officielle!

## ✨ Fonctionnalités

✅ **Upload de vidéos** - Upload une ou plusieurs vidéos automatiquement
✅ **Gestion des playlists** - Créer, modifier et gérer vos playlists
✅ **Statistiques** - Suivez les vues, likes, commentaires de vos vidéos
✅ **Édition vidéo** - Modifiez titres, descriptions, tags en masse
✅ **Miniatures** - Upload automatique de miniatures personnalisées
✅ **Menu interactif** - Interface utilisateur facile à utiliser

## 🚀 Installation rapide

### 1. Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte Google/YouTube
- Les credentials YouTube API

### 2. Cloner le repo

```bash
git clone https://github.com/yarismatiba-pixel/youtube-automation-animevortex.git
cd youtube-automation-animevortex
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les credentials YouTube

#### Étape 1: Créer une application Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet
3. Allez dans "APIs & Services" → "Enabled APIs & services"
4. Recherchez et activez "YouTube Data API v3"

#### Étape 2: Créer les credentials OAuth

1. Allez dans "APIs & Services" → "Credentials"
2. Cliquez sur "Create Credentials" → "OAuth client ID"
3. Sélectionnez "Desktop application"
4. Téléchargez le fichier JSON et renommez-le `credentials.json`
5. Placez-le à la racine du projet

#### Étape 3: Configurer les variables d'environnement

1. Copiez `.env.example` vers `.env`
2. Remplissez avec vos informations:

```env
# Obtenir votre CHANNEL_ID:
# 1. Allez sur https://www.youtube.com/account/advanced_account
# 2. Copiez l'ID de chaîne

YOUTUBE_CLIENT_ID=votre_client_id
YOUTUBE_CLIENT_SECRET=votre_client_secret
CHANNEL_ID=votre_channel_id
CHANNEL_NAME=AnimeVortex
DEFAULT_CATEGORY_ID=24
DEFAULT_LANGUAGE=fr
```

## 📖 Guide d'utilisation

### Lancer le menu principal

```bash
python main.py
```

### 1️⃣ Upload une seule vidéo

```bash
python main.py
# Sélectionnez option 1
```

**Exemple:**
- Chemin vidéo: `./my_video.mp4`
- Titre: `Top 10 Anime Moments`
- Description: `Découvrez les meilleures scènes de 2024!`
- Tags: `anime, top10, action`
- Miniature: `./thumbnail.jpg`

### 2️⃣ Upload plusieurs vidéos

Créez un fichier JSON `videos.json`:

```json
[
    {
        "path": "./videos/video1.mp4",
        "title": "Top 10 Anime Explosions",
        "description": "Découvrez les meilleures explosions anime!",
        "tags": ["anime", "explosions", "action"],
        "thumbnail": "./thumbnails/thumb1.jpg",
        "is_public": true,
        "playlist_id": null
    },
    {
        "path": "./videos/video2.mp4",
        "title": "Best Anime Fights",
        "description": "Les meilleurs combats de 2024!",
        "tags": ["anime", "fights", "epic"],
        "thumbnail": "./thumbnails/thumb2.jpg",
        "is_public": false,
        "playlist_id": "PLxxxxxxxxxxxx"
    }
]
```

Puis lancez:
```bash
python main.py
# Sélectionnez option 2
# Entrez le chemin: videos.json
```

Consultez `videos_batch_example.json` pour un exemple complet.

### 3️⃣ Gérer les playlists

```bash
python main.py
# Sélectionnez option 3

# Options:
# 1 - Voir toutes vos playlists
# 2 - Créer une nouvelle playlist
# 3 - Ajouter des vidéos à une playlist
```

**Créer une playlist:**
```
Titre: Best Anime of 2024
Description: Une compilation des meilleurs animes
Public? o/n: o
```

### 4️⃣ Voir les statistiques

```bash
python main.py
# Sélectionnez option 4

# Options:
# 1 - Stats globales de la chaîne
# 2 - Stats des 10 dernières vidéos
# 3 - Top vidéos par vues
```

Affiche:
- Nombre d'abonnés
- Vues totales
- Nombre de vidéos
- Stats individuelles (vues, likes, commentaires)

### 5️⃣ Modifier les vidéos

```bash
python main.py
# Sélectionnez option 5

# Options:
# 1 - Modifier le titre
# 2 - Modifier la description
# 3 - Modifier les tags
# 4 - Ajouter un footer à la description
```

**Exemple - Mettre à jour la description:**
```
ID de la vidéo: dQw4w9WgXcQ
Nouvelle description: 
Salut! Voici ma nouvelle description.
N'oublie pas de t'abonner!
```

## 💻 Scripts Python directs

### Utiliser dans vos propres scripts

```python
from youtube_uploader import YouTubeUploader
from youtube_stats import YouTubeStats
from youtube_playlists import YouTubePlaylistManager

# Upload une vidéo
uploader = YouTubeUploader()
result = uploader.upload_video(
    video_path='./mon_video.mp4',
    title='Mon titre',
    description='Ma description',
    tags=['anime', 'action'],
    is_public=True
)

# Voir les stats
stats = YouTubeStats()
stats.display_recent_videos_stats(5)
stats.display_top_videos(10)

# Gérer les playlists
pm = YouTubePlaylistManager()
playlists = pm.get_playlists()
pm.create_playlist('Ma playlist', 'Description')
```

## 📋 Structure du projet

```
youtube-automation-animevortex/
├── main.py                      # Menu principal interactif
├── youtube_auth.py              # Authentification OAuth
├── youtube_uploader.py          # Upload de vidéos
├── youtube_playlists.py         # Gestion des playlists
├── youtube_stats.py             # Statistiques
├── youtube_editor.py            # Édition des vidéos
├── requirements.txt             # Dépendances Python
├── .env.example                 # Template des variables d'environnement
├── .env                         # Variables d'environnement (à créer)
├── credentials.json             # Credentials YouTube (à créer)
├── videos_batch_example.json    # Exemple pour upload en masse
└── README.md                    # Ce fichier
```

## ⚙️ Configuration avancée

### Changer la catégorie vidéo

Les catégories YouTube disponibles:
- 24: Divertissement
- 25: Comédie  
- 20: Gaming
- 10: Musique
- 23: Comédie court métrage

Modifiez `DEFAULT_CATEGORY_ID` dans `.env`

### Ajouter automatiquement un footer

Modifiez `DEFAULT_DESCRIPTION_TEMPLATE` dans `.env`:

```env
DEFAULT_DESCRIPTION_TEMPLATE=Votre description
🔔 Abonnez-vous!
👍 Likez!
📺 Retrouvez plus sur ma chaîne
```

## 🔒 Sécurité

⚠️ **IMPORTANT:**
- Ne partagez JAMAIS votre fichier `credentials.json` ou `.env`
- Ajoutez-les à `.gitignore` (déjà fait)
- Les tokens sont sauvegardés dans `token.pickle` - gardez-le secret

## 🐛 Dépannage

### "Erreur: credentials.json non trouvé"
→ Téléchargez vos credentials depuis Google Cloud Console

### "Erreur: CHANNEL_ID non défini"
→ Remplissez correctement le fichier `.env`

### "Erreur: Vidéo trop grande"
→ YouTube limite à 256 GB, compressez votre vidéo

### "Erreur: Quota dépassé"
→ L'API YouTube a des limites quotidiennes (10,000 unités/jour)
→ Attendez 24h ou mettez à niveau votre quota

## 📚 Ressources

- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

## 📝 Licence

MIT License - Libre d'utilisation

## 💡 Conseils

1. **Testez d'abord en privé** avant de publier
2. **Utilisez des miniatures optimisées** (1280x720 pixels minimum)
3. **Attendez quelques secondes** entre les uploads en masse
4. **Faites des backups** de votre fichier `.env`
5. **Consultez les limites API** pour ne pas les dépasser

## 🤝 Contribuer

Les pull requests sont les bienvenues! Pour les changements majeurs, ouvrez d'abord une issue.

## 📞 Support

Des questions? Consultez:
- Les issues GitHub
- La documentation YouTube API
- Les exemples dans `videos_batch_example.json`

---

**Créé avec ❤️ pour AnimeVortex**

Bon upload! 🚀
````
