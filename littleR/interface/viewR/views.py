"""Views for the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    HttpResponse: The response object.
"""

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Standard_Model as Std
from littleR.tree import Tree
from littleR.tree_filter import TreeFilter
from .standard_view import StdView
from littleR.requirement import Requirement
from .forms.req_forms import ReqText, ReqPath, ReqLabel, ReqRelationParent, ReqRelationChild


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

@csrf_exempt
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
    
    # get the req content for the forms
    req_content = req.to_dict()
    
    #create the req_path_form, change the path
    rel_paths = standard.get_folio_relative_paths()
    abs_paths = standard.get_folio_paths()
    path_choices = [(abs,rel) for abs,rel in zip(abs_paths,rel_paths)]
    req_path_form = ReqPath(req_content, path_choices=path_choices )

    # create the req_text_form, edit the text
    req_text_form = ReqText(req_content)

    #create the template for the labels, this displays the labels for deletion
    label_template = loader.get_template("viewR/req_label.html")
    req_label = label_template.render({"req": req}, request)

    #create the label form, this lets the user add a new label
    req_label_form = ReqLabel(req_content)
    
    #create the template for related items, this displays the related items for deletion
    relation_template = loader.get_template("viewR/req_relation.html")
    req_relation = relation_template.render({"req": req}, request)

    #create the relation form, this lets the user add a new relation
    if req.is_customer():
        req_relation_form = ReqRelationChild(req_content)
    else:
        req_relation_form = ReqRelationParent(req_content)

    # use the template to display the requirement
    req_template = loader.get_template("viewR/req_detail.html")
    detail_content = {
        "req": req,
        "req_path_form": req_path_form,
        "req_text_form": req_text_form,
        "req_label": req_label,
        "req_label_form": req_label_form,
        "req_relation": req_relation,
        "req_relation_form": req_relation_form,
    }
    detail = req_template.render(detail_content, request)

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
