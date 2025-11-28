# Create your views here.
from django.shortcuts import render,redirect
# imported our models
from django.core.paginator import Paginator
from . models import Song
from django.contrib.auth.forms import UserCreationForm



# views.py

from django.core.serializers import serialize
import json

def index(request):
    songs_qs = Song.objects.all().order_by("title")
    paginator = Paginator(songs_qs, 1)  # show 1 track per page (you can increase)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # prepare minimal JSON for client-side playlist control
    songs_list = []
    for s in songs_qs:
        songs_list.append({
            'id': s.id,
            'title': s.title,
            'artist': s.artist,
            'image': s.image.url if s.image else '',
            'audio': s.audio_file.url if s.audio_file else s.audio_link,
            'lyrics': s.lyrics,  # ensure this is JSON text or escape it properly
            'lyrics_json': s.lyrics_json, 
        })

    return render(request, "main.html", {
        "page_obj": page_obj,
        "songs_json": json.dumps(songs_list),
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})