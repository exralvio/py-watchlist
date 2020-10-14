from .middleware import decode

def getUserID(request):
    token = request.headers.get('Authorization')
    user_data = decode(token)
    user_id = user_data["id"]

    return user_id