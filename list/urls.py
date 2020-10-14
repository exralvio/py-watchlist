from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('<int:list_id>/add_item', csrf_exempt(views.addItem), name = 'add'),
    path('<int:list_id>/remove_item', csrf_exempt(views.removeItem), name = 'remove'),
    path('<int:list_id>/clear', csrf_exempt(views.clearItem), name = 'clear'),

    path('', csrf_exempt(views.indexList), name = 'index'),
    path('<int:list_id>', csrf_exempt(views.showList), name = 'show')
]