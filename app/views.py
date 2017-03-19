"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from app.models import *
from twilio.rest import TwilioRestClient

def home(request):
    """Renders the home page."""
    if request.user.is_authenticated():
        return schedule_alarm(request)

    return render(
        request,
        'app/layout.html',
        {
            'title':'Home Page',
        }
    )
@login_required(login_url='/')
def main(request):
    pass

@login_required(login_url='/')
def active(request):
    profile = request.user.userprofile
    profile.active = True
    profile.save()
    return render(request, 'app/active.html', {'user_id':request.user.id})

@login_required(login_url='/')
def schedule_alarm(request):
    if request.method == 'POST':
        data = request.POST
        time_of_call = data.get('time_of_call')
        if time_of_call == '':
            time_of_call = datetime.datetime.now() + datetime.timedelta(minutes = 1)
        new_request = CallRequest.objects.create(requestee=request.user, description=data['description'], time_of_call=time_of_call)
        new_request.save()
        print("added request")
    return render(request, 'app/schedule_alarm.html', {'user_id':request.user.id})   

@login_required(login_url='/')
def call(request):
    data = request.POST
    request_phone_number = data.get('phone_number')
    request_id = data.get('request_id')
    # CLIENT 
    account_sid = "AC522687aea3e01be358218bfc878b4493"
    auth_token = "41be5156464d76f2b0150475e1aaf8e3"
    client = TwilioRestClient(account_sid, auth_token)

    call1 = client.calls.create(
           to=request.user.userprofile.phone_number, 
           from_="+17782002728", 
           url="https://handler.twilio.com/twiml/EH71f7a1a190bb7c849ae7501978e3ef80",  
           method="POST" 
        )

    call2 = client.calls.create(
           #to="+17788550329",
           to=request_phone_number,
           from_="+17782002728", 
           url="https://handler.twilio.com/twiml/EH71f7a1a190bb7c849ae7501978e3ef80",  
           method="POST" 
        )

    call_request = CallRequest.objects.get(id=request_id)
    call_request.is_pending = False
    call_request.is_completed = True
    call_request.completed_by = request.user
    call_request.save()

    return JsonResponse({'succeded': True})
