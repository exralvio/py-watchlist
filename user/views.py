import json
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from WatchList.response import Response
from WatchList.jwt import JWTAuth
from WatchList.middleware import jwtRequired
from . import transformer
from .models import Users
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        user = Users()
        user.name = json_data['name']
        user.email = json_data['email']
        user.password = make_password(password=json_data['password'])

        try:
            user.save()
        except IntegrityError:
            return Response.badRequest(message="Failed to register!")

        return Response.ok(
            values=transformer.singleTransform(user),
            message="Successfully Registered!"
        )
    else:
        return Response.badRequest(
            message="Invalid request."
        )

def auth(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        email = json_data['email']

        user = Users.objects.filter(email=email).first()

        if not user:
            return Response.badRequest(message="Email is not registered!")
        
        if not check_password(json_data['password'], user.password):
            return Response.badRequest(message="Wrong password!")

        user = transformer.singleTransform(user)

        jwt = JWTAuth()
        user['token'] = jwt.encode({"id": user['id']})

        return Response.ok(values=user, message="Login successfully!")
    else:
        return Response.badRequest(message="Invalid Request.")
