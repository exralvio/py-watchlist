from django.apps import AppConfig
from tmdbv3api import TMDb
from WatchList.settings import env

class MovieConfig(AppConfig):
    name = 'movie'

    def ready(self):
        tmdb = TMDb()
        tmdb.api_key = env('TMDB_API_KEY')
        tmdb.language = 'en'
        tmdb.debug = True
