import os
import json
from django.core.management.base import BaseCommand
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
                'image_file': 'Stay.jpeg',
                'lyrics_file': 'Stay.json'
            },
            {
                'title': 'Gabriela',
                'artist': 'KATSEYE',
                'duration': '3:08',
                'audio_file': 'Gabriela.mp3',
                'image_file': 'Gabriela.jpeg',
                'lyrics_file': 'Gabriela.json'
            },
            {
                'title': 'Paint the town red',
                'artist': 'Doja Cat',
                'duration': '3:50',
                'audio_file': 'DojaCat.mp3',
                'image_file': 'paint_the_town_red.jpeg',
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

        # Media folder paths - these are stored as paths, not uploaded
        LYRICS_FOLDER = os.path.join('media', 'lyrics')

        # Function to load lyrics from JSON
        def load_lyrics_from_json(lyrics_file):
            lyrics_path = os.path.join(LYRICS_FOLDER, lyrics_file)
            if not os.path.exists(lyrics_path):
                return '', None
            
            try:
                with open(lyrics_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle syncedlyrics format (array of {time, lyrics})
                    if isinstance(data, list):
                        lyrics_json_data = data
                        lyrics_text = '\n'.join([item.get('lyrics', '') for item in data if item.get('lyrics')])
                        return lyrics_text, lyrics_json_data
                    # Handle custom format {lyrics, lyrics_json}
                    elif isinstance(data, dict):
                        lyrics_text = data.get('lyrics', '')
                        lyrics_json_data = data.get('lyrics_json', None)
                        return lyrics_text, lyrics_json_data
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'  ✗ JSON error in {lyrics_file}: {str(e)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error reading {lyrics_file}: {str(e)}'))
            
            return '', None

        # Add songs to database
        for song_data in songs_data:
            try:
                # Construct file paths (just the path strings, not actual files)
                audio_path = f"audio/{song_data['audio_file']}"
                image_path = f"images/{song_data['image_file']}"
                
                # Load lyrics from JSON file
                lyrics_text, lyrics_json_data = load_lyrics_from_json(song_data['lyrics_file'])

                # Create or update song with file PATHS only
                song, created = Song.objects.update_or_create(
                    title=song_data['title'],
                    defaults={
                        'artist': song_data['artist'],
                        'duration': song_data['duration'],
                        'lyrics': lyrics_text,
                        'lyrics_json': lyrics_json_data,
                        'audio_file': audio_path,  # Store path as string
                        'image': image_path,  # Store path as string
                        'audio_link': '',
                    }
                )

                if lyrics_json_data:
                    self.stdout.write(f'  ✓ Lyrics: {len(lyrics_json_data) if isinstance(lyrics_json_data, list) else "loaded"}')
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Added: {song.title} by {song.artist}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'→ Updated: {song.title}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error with {song_data["title"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\nDone!'))