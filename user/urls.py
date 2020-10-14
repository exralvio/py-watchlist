from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', csrf_exempt(views.register), name = 'register'),
    path('auth', csrf_exempt(views.auth), name = 'auth'),
]