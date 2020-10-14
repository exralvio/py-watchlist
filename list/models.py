from django.db import models
from datetime import datetime

class Lists(models.Model):
    user_id = models.IntegerField(null=False)
    name = models.CharField(max_length=100, null=False)
    note = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'lists'

    
class ListMovies(models.Model):
    user_id = models.IntegerField(null=False)
    list_id = models.IntegerField(null=False)
    movie_id = models.IntegerField(null=False)
    title = models.CharField(max_length=250, null=True)
    poster_path = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(datetime.utcnow)

    class Meta:
        db_table = 'list_movies'