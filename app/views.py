"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def register(request):
    """Renders the about page."""
    return render(
        request,
        'app/register.html',
        {
            'title':'Registration',
            'year':datetime.now().year,
        }
    )
