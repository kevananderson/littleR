"""Views for supporting ajax in the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    JsonResponse: The response object.
"""

from django.http import HttpResponseNotFound, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Standard_Model as Std
from littleR.requirement import Requirement
from .forms.req_forms import ReqText, ReqPath, ReqLabel

def check_input(request, req_id):
    """Check the input for the requirement ID."""
    #check the req_id
    if not isinstance(req_id, str):
        return (False, "The requirement ID must be a string.", None, None)
    if not Requirement.valid_index(req_id):
        return (False, "The requirement ID is not valid.", None, None)

    # get the tree data
    standard = Std.model()

    # get the requirement
    req = standard.get_requirement(req_id)
    if req is None:
        return (False, "The requirement was not found.", None, None)
        
    # we get here via post
    if request.method != "POST":
        return (False, "The request must be a POST.", None, None)
        
    #regardless, the form must send the requirement index
    if "index" not in request.POST:
        return (False, "The requirement index is missing from the form.", None, None)
        
    #check the form index and the url match    
    form_index = request.POST["index"]
    if form_index != req.index:
        return (False, "The requirement index does not match the form index.", None, None)

    return (True, "", standard, req)

@csrf_exempt
def req_path(request, req_id):
    """The ajax handler for the requirement path."""
    (valid, message, standard, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    #create the choices for the form
    rel_paths = standard.get_folio_relative_paths()
    abs_paths = standard.get_folio_paths()
    path_choices = [(abs,rel) for abs,rel in zip(abs_paths,rel_paths)]

    #build the form
    form = ReqPath(request.POST, path_choices=path_choices)
    if form.is_valid():
        re_link = req.update_from_dict(form.cleaned_data)
        if re_link:
            pass #we need to relink this requirement not sure how yet
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'message': "The form is not valid."})

@csrf_exempt
def req_text(request, req_id):
    """The ajax handler for the requirement text."""
    (valid, message, _, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    #build the form
    form = ReqText(request.POST)
    if form.is_valid():
        req.update_from_dict(form.cleaned_data)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@csrf_exempt
def delete_req_label(request, req_id):
    """The ajax handler to delete labels from the requirement."""
    (valid, message, _, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    # check that the label is in the request
    if "label" not in request.POST:
        return JsonResponse({'success': False, 'message': "The label is missing from the form."})
    
    label = request.POST["label"]
    req.delete_label(label)

    #create the template for the labels, this displays the labels for deletion
    label_template = loader.get_template("viewR/req_label.html")
    req_label = label_template.render({"req": req}, request)

    return JsonResponse({'success': True, 'req_label': req_label})

@csrf_exempt
def add_req_label(request, req_id):
    """The ajax handler to add labels for the requirement."""
    (valid, message, _, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    # check that the label is in the request
    if "new_label" not in request.POST:
        return JsonResponse({'success': False, 'message': "The new_label is missing from the form."})
    
    label = request.POST["new_label"]
    req.add_label(label)

    #create the template for the labels
    label_template = loader.get_template("viewR/req_label.html")
    req_label = label_template.render({"req": req}, request)

    return JsonResponse({'success': True, 'req_label': req_label})

@csrf_exempt
def delete_req_relation(request, req_id):
    """The ajax handler to delete relationships from the requirement."""
    (valid, message, standard, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    # check that the label is in the request
    if "delete" not in request.POST:
        return JsonResponse({'success': False, 'message': "The information is missing from the form."})
    
    delete = request.POST["delete"]
    relink = req.delete_relationship(delete)
    if len(relink) >= 2:
        standard.relink(relink)

    #create the template for the relations, this displays the relations for deletion
    relation_template = loader.get_template("viewR/req_relation.html")
    req_relation = relation_template.render({"req": req}, request)

    return JsonResponse({'success': True, 'req_relation': req_relation})

@csrf_exempt
def add_req_relation(request, req_id):
    """The ajax handler to add relationships for the requirement."""
    (valid, message, standard, req) = check_input(request, req_id)

    if not valid:
        return JsonResponse({'success': False, 'message': message})
    
    # check that the label is in the request
    relink = []
    if req.is_customer():
        if "new_child" not in request.POST or "new_related" not in request.POST:
            return JsonResponse({'success': False, 'message': "The child or related index is missing from the form."})
        
        #add the relationship
        new_child = request.POST["new_child"]
        if Requirement.valid_index(new_child):
            relink.extend( req.add_relationship(new_child,'child') )
        new_related = request.POST["new_related"]
        if Requirement.valid_index(new_related):
            relink.extend( req.add_relationship(new_related,'related') )
        
    else:
        if "new_parent" not in request.POST or "new_related" not in request.POST:
            return JsonResponse({'success': False, 'message': "The parent or related index is missing from the form."})
        
        #add the relationship
        new_parent = request.POST["new_parent"]
        if Requirement.valid_index(new_parent):
            relink.extend( req.add_relationship(new_parent,'parent') )
        new_related = request.POST["new_related"]
        if Requirement.valid_index(new_related):
            relink.extend( req.add_relationship(new_related,'related') )

    #relink the requirements in the standard
    if len(relink) >= 2:
        standard.relink(relink)

    #create the template for the relations
    relation_template = loader.get_template("viewR/req_relation.html")
    req_relation = relation_template.render({"req": req}, request)

    return JsonResponse({'success': True, 'req_relation': req_relation})

