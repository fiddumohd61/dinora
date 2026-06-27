from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages

from foodapp.models import Restaurant


def customer_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:

            if Restaurant.objects.filter(owner=request.user).exists():

                messages.info(
                    request,
                    "You are logged in as a restaurant owner. Please use the restaurant dashboard."
                )

                return redirect("restaurant_dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper