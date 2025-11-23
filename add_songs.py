import os
import json
import django
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicPlayer.settings')
django.setup()

from App.models import Song

# Define your songs with their file names
songs_data = [
    {
        'title': 'Stay',
        'artist': 'Justin Bieber',
        'duration': '2:15',
        'audio_file': 'Stay.mp3',
        'image_file': 'Stay.jpg',
        'lyrics_file': 'Stay.json'  # New: JSON file for lyrics
    },
    {
        'title': 'Gabriela',
        'artist': 'KATSEYE',
        'duration': '3:08',
        'audio_file': 'Gabriela.mp3',
        'image_file': 'Gabriela.jpg',
        'lyrics_file': 'Gabriela.json'
    },
    {
        'title': 'Paint the town red',
        'artist': 'Doja Cat',
        'duration': '3:50',
        'audio_file': 'DojaCat.mp3',
        'image_file': 'paint_the_town_red.jpg',
        'lyrics_file': 'paint_the_town_red.json'
    },
    {
        'title': 'Hua Main from Movie: Animal',
        'artist': 'Pritam Chakraborty',
        'duration': '4:29',
        'audio_file': 'Hua_Main_Animal.mp3',
        'image_file': 'hua-main-animal-500-500.jpg',
        'lyrics_file': 'Hua_main.json'
    },
    {
        'title': 'Rockstar',
        'artist': 'Post Malone',
        'duration': '4:31',
        'audio_file': 'Post_Malone_rockstar.mp3',
        'image_file': 'postmalone.jpg',
        'lyrics_file': 'Rockstar.json'
    },
]

# Media folder paths
MEDIA_ROOT = 'media'
AUDIO_FOLDER = os.path.join(MEDIA_ROOT, 'audio')
IMAGE_FOLDER = os.path.join(MEDIA_ROOT, 'images')
LYRICS_FOLDER = os.path.join(MEDIA_ROOT, 'lyrics')

# Function to load lyrics from JSON
def load_lyrics_from_json(lyrics_path):
    try:
        with open(lyrics_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('lyrics', '')
    except Exception as e:
        print(f"✗ Error reading lyrics file {lyrics_path}: {str(e)}")
        return ''

# Add songs to database
for song_data in songs_data:
    try:
        # Construct file paths
        audio_path = os.path.join(AUDIO_FOLDER, song_data['audio_file'])
        image_path = os.path.join(IMAGE_FOLDER, song_data['image_file'])
        lyrics_path = os.path.join(LYRICS_FOLDER, song_data['lyrics_file'])
        
        # Load lyrics from JSON file
        lyrics_text = load_lyrics_from_json(lyrics_path)
        
        # Create song object
        song, created = Song.objects.get_or_create(
            title=song_data['title'],
            defaults={
                'artist': song_data['artist'],
                'duration': song_data['duration'],
                'lyrics': lyrics_text,
                'audio_link': '',
            }
        )
        
        # Add audio file if it exists
        if os.path.exists(audio_path):
            with open(audio_path, 'rb') as audio:
                song.audio_file.save(
                    song_data['audio_file'],
                    File(audio),
                    save=True
                )
            print(f"  ✓ Audio: {song_data['audio_file']}")
        else:
            print(f"  ✗ Audio not found: {audio_path}")
        
        # Add image file if it exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                song.image.save(
                    song_data['image_file'],
                    File(img),
                    save=True
                )
            print(f"  ✓ Image: {song_data['image_file']}")
        else:
            print(f"  ✗ Image not found: {image_path}")
        
        # Add lyrics from JSON
        if lyrics_text:
            print(f"  ✓ Lyrics loaded from: {song_data['lyrics_file']}")
        else:
            print(f"  ✗ No lyrics found in: {song_data['lyrics_file']}")
        
        if created:
            print(f"✓ Added song: {song.title} by {song.artist}\n")
        else:
            print(f"→ Updated song: {song.title}\n")
            
    except Exception as e:
        print(f"✗ Error adding {song_data['title']}: {str(e)}\n")

print("Done!")