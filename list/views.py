import json
from django.shortcuts import render
from WatchList.response import Response
from WatchList.middleware import jwtRequired
from WatchList.helpers import getUserID
from .models import Lists, ListMovies
from . import transformer
from django.utils import timezone
from django.http import JsonResponse
from activity import log


@jwtRequired
def addItem(request, list_id):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        movie_id = json_data["movie_id"]

        # Validate to make sure list is exists
        find_list = Lists.objects.filter(id=list_id).first()
        if not find_list:
            return Response.badRequest(message="Could not found the list.")

        # Validate to prevent duplicated movie in list
        find_movie = ListMovies.objects.filter(list_id=list_id, movie_id=movie_id).first()
        if find_movie:
            return Response.badRequest(message="Movie is already added.")

        user_id = getUserID(request)

        # Insert new movie into list
        model = ListMovies()
        model.user_id = user_id
        model.list_id = list_id
        model.movie_id = movie_id
        model.title = json_data["title"]
        model.poster_path = json_data["poster_path"]
        model.save()

        # log
        log.logger(user_id=user_id, ref='list_item', ref_id=model.id, action='add')

        return Response.ok(values=transformer.singleMovie(model), message="Movie successfully added.")
    else:
        return Response.badRequest()

@jwtRequired
def removeItem(request, list_id):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # Prevent empty movie ID
        movie_id = json_data["movie_id"]
        if not movie_id:
            return Response.badRequest(message="Movie ID is Required!")

        # Prevent delete others movie
        user_id = getUserID(request)
        find_movie = ListMovies.objects.filter(user_id=user_id, list_id=list_id, movie_id=movie_id).first()
        if not find_movie:
            return Response.badRequest(message="Selected movie is not found.")
        
        ref_id = find_movie.id
        find_movie.delete()

        log.logger(user_id=user_id, ref='list_item', ref_id=ref_id, action='remove')

        return Response.ok(message="Movie deleted from the list.")
    else:
        return Response.badRequest()

@jwtRequired
def clearItem(request, list_id):
    if request.method == 'POST':
        # Clear movies belongs by list
        find_movie = ListMovies.objects.filter(list_id=list_id).delete()

        user_id = getUserID(request)

        log.logger(user_id=user_id, ref='list', ref_id=list_id, action='clear')

        return Response.ok(message="List successfully cleared.")
    else:
        return Response.badRequest()

@jwtRequired
def indexList(request):
    if request.method == 'GET':
        return retrieveList(request)
    if request.method == 'POST':
        return addList(request)
    else:
        return Response.badRequest(message="Invalud request!")

def retrieveList(request):
    user_id = getUserID(request)

    # Retrieve all list belongs by user
    find_list = Lists.objects.filter(user_id=user_id).all()
    results = transformer.transform(find_list)

    return Response.ok(values=results)

def addList(request):
    json_data = json.loads(request.body)

    # Prevent empty list name
    if not json_data["name"]:
        return Response.badRequest(message="List name is required!")

    user_id = getUserID(request)

    # Insert new list
    insert_list = Lists()
    insert_list.user_id = user_id
    insert_list.name = json_data["name"]
    insert_list.note = json_data["note"]
    insert_list.save()

    log.logger(user_id=user_id, ref='list', ref_id=insert_list.id, action='add')

    return Response.ok(values=transformer.singleTransform(insert_list), message="List successfully added.")

@jwtRequired
def showList(request, list_id):
    if request.method == 'GET':
        return viewList(request, list_id)
    if request.method == 'PUT':
        return updateList(request, list_id)
    if request.method == 'DELETE':
        return deleteList(request, list_id)
    else:
        return Response.badRequest(message="Invalid request!")

def viewList(request, list_id):
    user_id = getUserID(request)

    # Retrieve one list by list_id
    find_list = Lists.objects.filter(id=list_id, user_id=user_id).first()
    
    # Prevent undefined List
    if not find_list:
        return Response.badRequest(message="Could not found the list.")

    # Init response as List detail
    response = transformer.singleTransform(find_list)

    # Retrieve movies from the List
    movies = ListMovies.objects.filter(list_id=find_list.id).all()

    # Append movies to arr of items
    response["items"] = transformer.transformMovies(movies)
    
    return JsonResponse(response)

def updateList(request, list_id):
    user_id = getUserID(request)

    # Prevent update others list
    find_list = Lists.objects.filter(user_id=user_id, id=list_id).first()
    if not find_list:
        return Response.badRequest(message="Could not find the list.")

    json_data = json.loads(request.body)

    # Prevent empty list name
    if not json_data['name']:
        return Response.badRequest(message="List name is required!")

    find_list.name = json_data['name']
    find_list.note = json_data['note']
    find_list.updated_at = timezone.now()
    find_list.save()

    log.logger(user_id=user_id, ref='list', ref_id=find_list.id, action='update')

    return Response.ok(message="List successfully updated.")

def deleteList(request, list_id):
    user_id = getUserID(request)

    # Prevent delete others list
    find_list = Lists.objects.filter(user_id=user_id, id=list_id).first()
    if not find_list:
        return Response.badRequest(message="Could not find the list.")

    # Clear movie belonging by the list
    delete_movie = ListMovies.objects.filter(list_id=list_id).delete()

    # Delete list
    find_list.delete()

    log.logger(user_id=user_id, ref='list', ref_id=list_id, action='delete')
    
    return Response.ok(message="List successfully deleted.")