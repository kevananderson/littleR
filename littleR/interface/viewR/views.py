"""Views for the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    HttpResponse: The response object.
"""

from django.http import HttpResponse
from django.template import loader
from .models import Standard_Model as Std
from littleR.tree import Tree
from littleR.tree_filter import TreeFilter
from .standard_view import StdView


def index(request):
    """The index view for the viewR app."""
    # get the tree data
    tree = Tree( Std.model(), TreeFilter({})) # no filter for now

    # toc_tree (table of contents tree)
    toc_list = StdView.toc_tree(request, tree, 4) #depth can also be changed

    # toc
    toc_template = loader.get_template("viewR/toc.html")
    toc = toc_template.render({"toc_list": toc_list}, request)

    # menu
    menu_template = loader.get_template("viewR/menu.html")
    menu = menu_template.render({"menu": ""}, request)

    # navigation
    navigation_template = loader.get_template("viewR/navigation.html")
    navigation = navigation_template.render({"navigation": ""}, request)

    # page
    page_content = {
        "content": toc,
        "menu": menu,
        "sidebar": navigation,
    }
    page_template = loader.get_template("viewR/page.html")
    page = page_template.render(page_content, request)

    return HttpResponse(page)
