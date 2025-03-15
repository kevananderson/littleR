"""Views for supporting pdf creation in the viewR app.

All the views have the same structure.

Args:
    request (HttpResponse): The request object.

Returns:
    JsonResponse: The response object.
"""
import os
import asyncio

PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteer import launch
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
        
    # pdf file name
    standard = Std.model()
    pdf_dir = os.path.join( standard.get_report_path(), "project" ).replace("\\", "/") 
    if not os.path.isdir(pdf_dir):
        os.makedirs(pdf_dir, exist_ok=True)

    # we do different things depending on if we are making a summary or detail
    if action == "summary":
        url = "http://localhost:8000/viewR/pdf/summary"
        filename = os.path.join( pdf_dir, "Project Summary.pdf" ).replace("\\", "/")
    elif action == "detail":
        url = "http://localhost:8000/viewR/pdf/detail"
        filename = os.path.join( pdf_dir, "Project Details.pdf" ).replace("\\", "/")
    return write_pdf(url, filename)

@csrf_exempt
def pdf_summary(request):
    """The summary view."""
    # pdf
    pdf_content = common_content(request, {"title": "Project Summary"} )
    pdf_content["menu"] = menu_rendered(request)
    pdf_content["content"] = StdView.summary(request, 100, pdf=True) #depth can also be changed

    # page
    page_template = loader.get_template("viewR/pdf_page.html")
    page_html = page_template.render(pdf_content, request)

    return HttpResponse(page_html)

def pdf_detail(request):
    """The detail view."""
    # pdf
    pdf_content = common_content(request, {"title": "Project Details"} )
    pdf_content["menu"] = menu_rendered(request)
    pdf_content["content"] = StdView.detail(request, 100, pdf=True) #depth can also be changed

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
    if "title" not in title_content:
        title_content["title"] = "Project Summary"
    if "desc" not in title_content:
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

def write_pdf(url, filename):
    """Write the pdf."""
    try:
        asyncio.new_event_loop().run_until_complete(generate_pdf(url, filename))
    except Exception:
        message = "PDF Error"
        return JsonResponse({'success': False, 'message': message})
    message = "PDF Written"
    return JsonResponse({'success': True, 'message': message})

async def generate_pdf(url, filename):
    """Generate the pdf."""
    browser = await launch(handleSIGINT=False, handleSIGTERM=False,handleSIGHUP=False)
    page = await browser.newPage()
    await page.goto(url)
    await page.pdf({'path': filename, 'format': 'letter'})
    await browser.close()