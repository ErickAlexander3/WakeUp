"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required

from twilio.rest import TwilioRestClient

def home(request):
    """Renders the home page."""
    if request.user.is_authenticated():
        return active(request)

    return render(
        request,
        'app/layout.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

@login_required(login_url='/')
def active(request):
    return render(request, 'app/active.html', {})   

def call(request):

    # CLIENT 
    account_sid = "AC522687aea3e01be358218bfc878b4493"
    auth_token = "41be5156464d76f2b0150475e1aaf8e3"
    client = TwilioRestClient(account_sid, auth_token)

    call1 = client.calls.create(
           to="+17783239437", 
           from_="+17782002728", 
           url="https://handler.twilio.com/twiml/EH71f7a1a190bb7c849ae7501978e3ef80",  
           method="POST" 
        )

    call2 = client.calls.create(
           #to="+17788550329",
           to="+18072201876",
           from_="+17782002728", 
           url="https://handler.twilio.com/twiml/EH71f7a1a190bb7c849ae7501978e3ef80",  
           method="POST" 
        )  
    return render()
