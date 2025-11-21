🎵 Django Music Player

A modern, fully-functional Django-based music player with playlists, synced lyrics, user authentication, and a clean, responsive UI.

🌟 Features

🎧 Music Player

-Play / Pause / Next / Previous track
-Real-time seek bar
-Volume control
-Auto-next on song end
-Stream uploaded audio files (MP3, WAV)

🎤 Synced Lyrics

-JSON timestamped lyrics
-LRC-format support
-Auto-scrolling lyric panel
-Current line highlighting

🎵 Playlist

-Dynamic playlist loaded from backend
-Click-to-play any track
-Artist / Title / Cover art displayed
-Fully integrated with player controls

🔐 User System

-Django Authentication system
-Custom Login page
-Custom Signup / Register page
-Optional profile image upload

🖥️ UI & UX

-Dark theme music app
-Card-based layout
-Responsive 3-column design
-Left: Playlist
-Center: Player
-Right: Lyrics
-Smooth animations & clean typography

🛠️ Tech Stack

Layer	Technology
Backend - Django 4.x
Frontend - HTML, CSS, JS, Font Awesome
Media Handling	- <audio> API
Database	SQLite (default)
Authentication	Django Auth (Login, Logout, Register)

📂 Project Structure
MusicPlayer/
│
├── App/
│   ├── migrations/
│   ├── templates/
│   │   ├── main.html
│   │   ├── login.html
│   │   ├── register.html
│   ├── static/
│   │   ├── style.css
│   │   ├── script.js
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── MusicPlayer/
│   ├── settings.py
│   ├── urls.py
│
├── media/
│   ├── songs/
│   ├── covers/
│
├── manage.py
└── README.md

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/Tavisha10/Music-Player-App.git
cd Music-Player-App

2️⃣ Create and Activate Virtual Environment
python -m venv env
env\Scripts\activate   # Windows
source env/bin/activate # macOS / Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start Development Server
python manage.py runserver


Visit http://127.0.0.1:8000/
 to view the app.

🎶 Adding Songs

-Via Django Admin
-First create a superuser:
-python manage.py createsuperuser
-Log into /admin/ and add:
--Title
--Artist
--Audio file or Audio URL
--Cover image
--Lyrics JSON or LRC
--Lyrics JSON Format
[
  { "time": "0:12", "lyrics": "First line" },
  { "time": "0:18", "lyrics": "Second line" }
]
--LRC Format
--[00:12.00] First line
--[00:18.40] Second line

📌 Known Issues

-Seeking may not work for audio hosted without CORS metadata
-Autoplay can be blocked by browsers
-Heavy MP3 files may load slowly

🧩 Future Enhancements

-Add “Favorites” feature
-Waveform audio visualizer
-User playlists
-Drag-and-drop queue
-Search bar for songs



👩‍💻 Author

Tavisha
Passionate developer building music, AI, and full-stack projects.
GitHub: https://github.com/Tavisha10
