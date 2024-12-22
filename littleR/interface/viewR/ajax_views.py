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
from .forms.req_forms import ReqText

@csrf_exempt
def req_text(request, req_id):
    """The ajax handler for the requirement."""
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

    # we get here via post
    if request.method != "POST":
        return HttpResponseNotFound("The request must be a POST.")

    #regardless, the form must send the requirement index
    if "index" not in request.POST:
        return HttpResponseNotFound("The requirement index is missing from the form.")

    #check the form index and the url match    
    form_index = request.POST["index"]
    if form_index != req.index:
        return HttpResponseNotFound("The requirement index does not match the form index.")
    
    #build the form
    form = ReqText(request.POST)
    if form.is_valid():
        re_link = req.update_from_dict(form.cleaned_data)
        if re_link:
            pass #we need to relink this requirement not sure how yet
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})