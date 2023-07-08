from .views import getavatar


def avatar_context_processor(request):
    avatar = getavatar(request)
    return {'avatar': avatar}
