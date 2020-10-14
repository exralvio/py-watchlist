from tmdbv3api import Movie
from . import transformer
from WatchList.response import Response
from WatchList.middleware import jwtRequired

@jwtRequired
def popular(request):
    if request.method == 'GET':
        movie = Movie()
        popular = movie.popular()

        results = transformer.transform(popular)

        return Response.ok(results)
    else:
        return Response.badRequest(message="Invalid request")

@jwtRequired
def top_rated(request):
    if request.method == 'GET':
        movie = Movie()
        latest = movie.top_rated()

        results = transformer.transform(latest)

        return Response.ok(results)
    else:
        return Response.badRequest(message="invalid request")
