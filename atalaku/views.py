from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from atalaku import settings

    

def page_not_found(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error(request):
    template_name = '500.html'
    return render(request, template_name)

def permission_denied(request):
    template_name = '500.html'
    return render(request, template_name)

def bad_request(request):
    template_name = '500.html'
    return render(request, template_name)



def home(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "home.html"
    page_title = settings.SITE_NAME
    context = {
        'page_title': page_title,
        'site_name': settings.SITE_NAME
    }
    return render(request, template_name,context)


def about(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "about.html"
    page_title = 'A Propose | ' + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)



def faq(request):
    template_name = "faq.html"
    page_title = "FAQ | " + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)


def privacy_policy(request):
    template_name = "privacy_policy.html"
    page_title =  UI_STRINGS.UI_PRIVACY_POLICY+ ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)


def terms_of_use(request):
    template_name = "terms_of_use.html"
    page_title =  UI_STRINGS.UI_TERMS_OF_USE + ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)