from django.http import HttpResponse
from django.template import loader
#from django.shortcuts import render

#from context import littleR
#from littleR.standard import Standard
from .models import Standard_Model as Std


def index(request):
    """The index view for the viewR app.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    # get the tree data
    depth_tree = Std.model().depth_tree()
    
    edited_tree = []
    for d,req in depth_tree:
        if d <= 0:
            continue
        if d > 7:
            d = 7
        edited_tree.append((d,req))

    # tree (table of contents)
    tree_template = loader.get_template("viewR/toc_tree.html")
    tree = tree_template.render({"tree": edited_tree}, request)

    # index
    index_template = loader.get_template("viewR/index.html")
    index = index_template.render({"tree": tree}, request)

    # page
    page_template = loader.get_template("viewR/page.html")
    page = page_template.render({"body": index}, request)

    return HttpResponse(page)
