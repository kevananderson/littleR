"""Views for supporting pdf creation in the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    JsonResponse: The response object.
"""
import os
from xhtml2pdf import pisa
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Standard_Model as Std
from .views import menu_rendered
from .standard_view import StdView
from littleR.tree import Tree
from littleR.tree_filter import TreeFilter
from littleR.requirement import Requirement

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

    #enable pisa logging
    pisa.showLogging()

    #collect variables needed specifically for the pdf
    standard = Std.model()
    meta_title = "PDF Summary"
    static_root = str(settings.BASE_DIR) + "/viewR/static/viewR"
    
    # pdf
    title_content = {
        "static_root": static_root,
        "image_name": "project_logo.png",
    }
    pdf_content = common_content(request, title_content)
    pdf_content["content"] = StdView.summary(request, 100) #depth can also be changed
    pdf_content["meta_title"] = meta_title
    pdf_content["static_root"] = static_root

    pdf_template = loader.get_template("viewR/pdf.html")
    pdf_html = pdf_template.render(pdf_content, request)
    
    # write the pdf
    pdf_dir = os.path.join( standard.get_report_path(), "project" ).replace("\\", "/") 
    if not os.path.isdir(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)

    pdf_filename = os.path.join( pdf_dir, "Project Summary.pdf" ).replace("\\", "/")
    with open(pdf_filename, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(pdf_html, dest=pdf_file)

        if pisa_status.err:
            message = "Error writing the PDF."
            return JsonResponse({'success': False, 'message': message})

    message = "Summary Written"
    return JsonResponse({'success': True, 'message': message})

def preview_summary(request):
    """The preview summary view."""

    # pdf
    pdf_content = common_content(request)
    pdf_content["menu"] = menu_rendered(request)
    pdf_content["content"] = StdView.summary(request, 100) #depth can also be changed

    # page
    page_template = loader.get_template("viewR/pdf_page.html")
    page_html = page_template.render(pdf_content, request)

    return HttpResponse(page_html)

def pdf_detail(request):
    message = "pdf_detail not yet defined."
    return JsonResponse({'success': False, 'message': message})

def preview_detail(request):
    """The preview detail view."""

    #collect variables needed specifically for the preview
    menu_html = menu_rendered(request)

    # pdf
    pdf_content = common_content(request)
    pdf_content["menu"] = menu_html

    # page
    page_template = loader.get_template("viewR/pdf_page.html")
    page_html = page_template.render(pdf_content, request)

    return HttpResponse(page_html)

# helper functions

def common_content(request, title_content=None):
    """The content for the summary pdf."""

    #verify the input
    if title_content is None:
        title_content = {}
    if not isinstance(title_content, dict):
        raise TypeError("The title content must be a dictionary.")
    
    #title page
    title_content["title"] = "Project Summary"
    title_content["desc"] = "Requirements for the Project."
    title_content["version"] = "0.0.1"
    title_content["date"] = "January 15, 2025"
    #title_content["line_1"] = ""
    #title_content["line_2"] = ""
    #title_content["line_3"] = ""
    #title_content["line_4"] = ""
    title_html = render_title(title_content,request)

    # table of contents
    toc_html = StdView.toc(request, 4, pdf=True) #depth can also be changed

    # summary content


    pdf_content = {
        "title": title_html,
        "toc": toc_html,
    }

    return pdf_content

def render_title( content, request ):
    """The title page for the PDF."""
    
    # verify content
    if not isinstance(content, dict):
        raise TypeError("The content must be a dictionary.")
    expected = ["title", "desc", "version", "date"]
    for key in expected:
        if key not in content:
            raise KeyError("The content must have a key: " + key)
        
    title_template = loader.get_template("viewR/pdf_title.html")
    title_html = title_template.render(content, request)
    return title_html