from django.http import Http404
from app.models import Group
from django.shortcuts import render

def check_user_able_to_see_page(*groups: Group):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(
                name__in=[group.name for group in groups]
            ).exists():
                return function(request, *args, **kwargs)
            return render(request, "unauth_user.html")

        return wrapper

    return decorator