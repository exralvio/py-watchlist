from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('popular', csrf_exempt(views.popular), name = 'popular'),
    path('top_rated', csrf_exempt(views.top_rated), name = 'top_rated')
]