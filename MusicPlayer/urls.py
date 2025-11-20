# MusicPlayer/urls.py  (project-level)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Django's auth views (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    # include your application urls (App)
    path('', include('App.urls')),
]

# static + media in development
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
