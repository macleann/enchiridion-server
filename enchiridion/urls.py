"""
URL configuration for enchiridion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from enchiridionapi import views

router = DefaultRouter(trailing_slash=False)
router.register(r'episodes', views.EpisodeView, 'episode')
router.register(r'seasons', views.SeasonView, 'season')
router.register(r'user-playlists', views.UserPlaylistView, 'user-playlist')
router.register(r'playlists', views.PublicPlaylistView, 'playlist')
router.register(r'series', views.SeriesView, 'series')

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register_user),
    path('login', views.login_user),
    path('google/login', views.google_login),
    path('verify', views.verify_token),
    path('logout', views.logout_user),
    path('admin/', admin.site.urls),
]
