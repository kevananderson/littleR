"""Views for the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    HttpResponse: The response object.
"""

from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from .models import Standard_Model as Std
from littleR.tree import Tree
from littleR.tree_filter import TreeFilter
from .standard_view import StdView
from littleR.requirement import Requirement


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

def detail(request, req_id):
    """The detail view for the requirement."""
    # verify the input
    if not isinstance(req_id, str):
        return HttpResponseNotFound("The requirement ID must be a string.")
    if not Requirement.valid_index(req_id):
        return HttpResponseNotFound("The requirement ID is not valid.")
    
    # get the tree data
    standard = Std.model()

    # get the requirement
    req = standard.get_requirement(req_id)
    if req is None:
        return HttpResponseNotFound("The requirement was not found.")
    
    # use the template to display the requirement
    req_template = loader.get_template("viewR/req_detail.html")
    detail = req_template.render({"req": req}, request)

    # menu
    menu_template = loader.get_template("viewR/menu.html")
    menu = menu_template.render({"menu": ""}, request)

    # navigation
    navigation_template = loader.get_template("viewR/navigation.html")
    navigation = navigation_template.render({"navigation": ""}, request)

    # page
    page_content = {
        "content": detail,
        "menu": menu,
        "sidebar": navigation,
    }
    page_template = loader.get_template("viewR/page.html")
    page = page_template.render(page_content, request)

    return HttpResponse(page)
