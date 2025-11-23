import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from App.models import Song

class Command(BaseCommand):
    help = 'Add songs from media folder to database'

    def handle(self, *args, **options):
        songs_data = [
            {
                'title': 'Stay',
                'artist': 'Justin Bieber',
                'duration': '2:15',
                'audio_file': 'Stay.mp3',
                'image_file': 'Stay.jpg',
                'lyrics_file': 'Stay.json'
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
            # Add more songs here...
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
                self.stdout.write(self.style.WARNING(f'Error reading lyrics: {str(e)}'))
                return ''

        # Add songs to database
        for song_data in songs_data:
            try:
                # Construct file paths
                audio_path = os.path.join(AUDIO_FOLDER, song_data['audio_file'])
                image_path = os.path.join(IMAGE_FOLDER, song_data['image_file'])
                lyrics_path = os.path.join(LYRICS_FOLDER, song_data['lyrics_file'])

                # Load lyrics from JSON file
                lyrics_text = ''
                lyrics_json_data = None
                
                if os.path.exists(lyrics_path):
                    try:
                        with open(lyrics_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                            # Handle syncedlyrics format (array of {time, lyrics})
                            if isinstance(data, list):
                                lyrics_json_data = data
                                # Convert to plain text for lyrics field
                                lyrics_text = '\n'.join([item.get('lyrics', '') for item in data if item.get('lyrics')])
                            # Handle custom format {lyrics, lyrics_json}
                            elif isinstance(data, dict):
                                lyrics_text = data.get('lyrics', '')
                                lyrics_json_data = data.get('lyrics_json', None)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error reading lyrics: {str(e)}'))

                # Create or update song
                song, created = Song.objects.get_or_create(
                    title=song_data['title'],
                    defaults={
                        'artist': song_data['artist'],
                        'duration': song_data['duration'],
                        'lyrics': lyrics_text,
                        'lyrics_json': lyrics_json_data,
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
                    self.stdout.write(f'  ✓ Audio: {song_data["audio_file"]}')
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Audio not found: {audio_path}'))

                # Add image file if it exists
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img:
                        song.image.save(
                            song_data['image_file'],
                            File(img),
                            save=True
                        )
                    self.stdout.write(f'  ✓ Image: {song_data["image_file"]}')
                else:
                    self.stdout.write(self.style.WARNING(f'  ✗ Image not found: {image_path}'))

                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Added: {song.title} by {song.artist}\n'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'→ Updated: {song.title}\n'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error adding {song_data["title"]}: {str(e)}\n'))

        self.stdout.write(self.style.SUCCESS('Done!'))