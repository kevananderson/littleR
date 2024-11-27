from django.shortcuts import render  # noqa F401
from django.http import HttpResponse


# Create your views here.
def index(request):
    """The index view for the viewR app.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return HttpResponse("Hello World! viewR")
