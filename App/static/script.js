// script.js
  // init mediaelement for UI (optional), but we will control audio with plain JS
 /* $('audio').mediaelementplayer({
    audioHeight: 60,
    features: ['playpause','current','progress','volume'],
    alwaysShowControls: true
  }); */

  // script.js — minimal, replace your current file or patch accordingly
document.addEventListener('DOMContentLoaded', function () {
  // REMOVE or comment-out mediaelement init if present:
  // $('audio').mediaelementplayer({...});  // <= COMMENT OUT OR DELETE

  const audio = document.getElementById('fc-media');
  const playBtn = document.getElementById('playpause');
  const seek = document.getElementById('seek');
  const currentTimeEl = document.getElementById('current-time');
  const durationEl = document.getElementById('duration');
  const volume = document.getElementById('volume');
  const lyricsScroll = document.getElementById('lyrics-scroll');

  // playlist from DOM
  const songs = JSON.parse(document.getElementById('songs-data').textContent || "[]");
  let currentIndex = 0;

  // NEW loadTrack: set audio.src directly (important)
  function loadTrack(index) {
    if (!songs[index]) return;
    currentIndex = index;
    const track = songs[index];

    // set the real audio element's src — this is the reliable way
    audio.src = track.audio;
    audio.load(); // reload metadata and duration
    // update UI
    document.getElementById('cover-image').src = track.image || '';
    document.getElementById('track-title').innerText = track.title || '';
    document.getElementById('track-artist').innerText = track.artist || '';

    renderLyrics(track.lyrics);
  }

  function parseLyrics(lyricsRaw) {
    if (!lyricsRaw) return [];
    try {
      const parsed = JSON.parse(lyricsRaw);
      if (Array.isArray(parsed)) {
        return parsed.map(item => ({
          t: timeToSeconds(item.time || item.timestamp || item.t || "0:00"),
          text: item.lyrics || item.text || ''
        }));
      }
    } catch (e) {}
    // fallback to LRC-style
    const lines = (lyricsRaw || '').split(/\r?\n/);
    const out = [];
    lines.forEach(line => {
      const m = line.match(/\[(\d{1,2}:\d{2}(?:\.\d{1,2})?)\](.*)/);
      if (m) out.push({ t: timeToSeconds(m[1]), text: m[2].trim() });
    });
    return out;
  }

  function timeToSeconds(timeStr) {
    if (!timeStr) return 0;
    const parts = timeStr.split(':');
    const minutes = parseFloat(parts[0]) || 0;
    const seconds = parseFloat(parts[1]) || 0;
    return minutes * 60 + seconds;
  }

  function renderLyrics(lyricsRaw) {
    const arr = parseLyrics(lyricsRaw);
    lyricsScroll.innerHTML = '';
    arr.forEach((ln, i) => {
      const div = document.createElement('div');
      div.className = 'lyric-line';
      div.dataset.time = ln.t;
      div.dataset.index = i;
      div.innerText = ln.text;
      lyricsScroll.appendChild(div);
    });
    audio._lyrics = arr;
    audio._currentLyricIndex = 0;
  }

  audio.addEventListener('loadedmetadata', () => {
    durationEl.innerText = formatTime(audio.duration || 0);
    seek.max = Math.floor(audio.duration || 0);
  });

  audio.addEventListener('timeupdate', () => {
    currentTimeEl.innerText = formatTime(audio.currentTime || 0);
    seek.value = Math.floor(audio.currentTime || 0);

    // lyrics sync
    const list = audio._lyrics || [];
    if (list.length) {
      let i = audio._currentLyricIndex || 0;
      while (i < list.length - 1 && audio.currentTime >= list[i + 1].t - 0.1) i++;
      while (i > 0 && audio.currentTime < list[i].t - 0.5) i--;
      if (i !== audio._currentLyricIndex) {
        audio._currentLyricIndex = i;
        highlightLyric(i);
      }
    }
  });

  function highlightLyric(index) {
    const nodes = lyricsScroll.querySelectorAll('.lyric-line');
    nodes.forEach(n => n.classList.remove('current'));
    const cur = lyricsScroll.querySelector(`.lyric-line[data-index="${index}"]`);
    if (cur) {
      cur.classList.add('current');
      const top = cur.offsetTop - lyricsScroll.offsetTop - (lyricsScroll.clientHeight / 2) + (cur.clientHeight / 2);
      lyricsScroll.scrollTo({ top, behavior: 'smooth' });
    }
  }

  function formatTime(sec) {
    if (!isFinite(sec)) return "0:00";
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    const m = Math.floor(sec / 60);
    return `${m}:${s}`;
  }

  // controls
  playBtn.addEventListener('click', () => {
    if (audio.paused) { audio.play(); playBtn.innerHTML = '<i class="fa fa-pause"></i>'; }
    else { audio.pause(); playBtn.innerHTML = '<i class="fa fa-play"></i>'; }
  });

  // IMPORTANT: handle seeking by setting currentTime on the actual audio
  seek.addEventListener('input', () => {
    // ensure numeric and within range
    const val = Number(seek.value);
    if (!Number.isNaN(val)) audio.currentTime = val;
  });

  volume.addEventListener('input', () => {
    audio.volume = volume.value;
  });

  // build left playlist
  const plist = document.getElementById('playlist-list');
  if (plist) {
    plist.innerHTML = '';
    songs.forEach((s, idx) => {
      const li = document.createElement('li');
      li.className = 'playlist-item';
      li.innerHTML = `<img class="plist-thumb" src="${s.image || ''}" /><div class="plist-meta"><div class="plist-title">${s.title}</div><div class="plist-artist">${s.artist}</div></div>`;
      li.addEventListener('click', () => {
        loadTrack(idx);
        // nav feedback
        audio.play().then(() => {
          playBtn.innerHTML = '<i class="fa fa-pause"></i>';
        }).catch(err => {
          // autoplay might be blocked — still UI updated
          playBtn.innerHTML = '<i class="fa fa-play"></i>';
          console.warn('Could not autoplay:', err);
        });
      });
      plist.appendChild(li);
    });
  }

  document.getElementById('prev-track').addEventListener('click', () => {
    let next = (currentIndex - 1 + songs.length) % songs.length;
    loadTrack(next);
    audio.play(); playBtn.innerHTML = '<i class="fa fa-pause"></i>';
  });
  document.getElementById('next-track').addEventListener('click', () => {
    let next = (currentIndex + 1) % songs.length;
    loadTrack(next);
    audio.play(); playBtn.innerHTML = '<i class="fa fa-pause"></i>';
  });

  audio.addEventListener('ended', () => {
    document.getElementById('next-track').click();
  });

  // init
  if (songs.length) loadTrack(0);
});
