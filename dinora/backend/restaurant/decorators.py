from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from foodapp.models import Restaurant


def restaurant_owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            messages.error(
                request,
                "Please login as a restaurant owner."
            )

            return redirect("restaurant_login")

        restaurant = Restaurant.objects.filter(
            owner=request.user
        ).first()

        if restaurant is None:

            messages.error(
                request,
                "You are not authorized to access the restaurant dashboard."
            )

            return redirect("restaurant_login")

        return view_func(request, *args, **kwargs)

    return wrapper