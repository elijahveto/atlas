from django.http import HttpResponse
from django.shortcuts import redirect


# stop logged in user from viewing the register page or the login page
def unauthenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view(request, *args, **kwargs)
    return wrapper


# does not work on class views/ used group mixin instead

# def allowed_users(allowed=[]):
#     def decorator(view):
#         def wrapper(request, *args, **kwargs):
#             if request.request.user.groups.exists():
#                 group = request.request.user.groups.all()[0].name
#                 if group in allowed:
#                     return view(request.request, *args, **kwargs)
#                 else:
#                     return HttpResponse('you are not authorized to perform this action.')
#         return wrapper
#     return decorator
