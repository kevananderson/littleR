"""Views for supporting pdf creation in the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    JsonResponse: The response object.
"""

from django.http import JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Standard_Model as Std
from littleR.requirement import Requirement
from .forms.req_forms import ReqText, ReqPath


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
def pdf_write(request, action):
    """The ajax handler to make PDFs."""
    #check the action
    if not isinstance(action, str):
        message = "The action url is not correct."
        return JsonResponse({'success': False, 'message': message})

    # we get here via post
    if request.method != "POST":
        message = "The method must be POST."
        return JsonResponse({'success': False, 'message': message})
    
    #regardless, the form must send the requirement index
    valid_actions = ["summary", "detail"]
    if action not in valid_actions:
        message = "The action is not valid."
        return JsonResponse({'success': False, 'message': message})
        
    # we do different things depending on if we are making a summary or detail
    if action == "summary":
        return pdf_summary(request)
    elif action == "detail":
        return pdf_detail(request)

    message = "Action not defined."
    return JsonResponse({'success': False, 'message': message})

def pdf_summary(request):

    message = "Summary Written."
    return JsonResponse({'success': True, 'message': message})

def pdf_detail(request):
    message = "pdf_detail not yet defined."
    return JsonResponse({'success': False, 'message': message})
