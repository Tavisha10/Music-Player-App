from django.db import models

class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField()
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    
    # Human-readable lyrics (LRC-like text)
    lyrics = models.TextField(blank=True, null=True)

    # Original time-coded JSON for syncing
    lyrics_json = models.JSONField(blank=True, null=True)  # Django >= 3.1

    duration = models.CharField(max_length=20)

    paginate_by = 2

    def __str__(self):
        return self.title
