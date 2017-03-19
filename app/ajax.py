"""
Views that will be used exclusively for ajax requests
"""

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import RequestContext
from django.contrib.auth import login
from datetime import datetime
from django.contrib.auth.decorators import login_required

from app.forms import *
from django.contrib.auth import get_user_model
from app.models import UserProfile, CallRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from time import time


def login_or_register(request):
    ##only allow ajax requests
    #if not request.is_ajax():
    #    return
    request_data = request.POST
    server_data = {}
    username = request_data.get('username')
    password = request_data.get('password')
    print(username, password)
    #register only if username and phone number don't exist in the database
    user = authenticate(username=username, password=password)
    if user is None:
        server_data['logged'] = False
    else:
        login(request, user)
        server_data['logged'] = True

    return JsonResponse(server_data)


def register(request):
    request_data = request.POST
    server_data = {}
    username = request_data.get('username')
    password = request_data.get('password')
    phone_number = request_data.get('phone_number')
    email = request_data.get('email')
    print(username, password, phone_number, email)
    if not User.objects.filter(username=username).exists() and not UserProfile.objects.filter(phone_number=phone_number).exists():
        new_user = User.objects.create_user(username, email, password)
        new_user_profile = UserProfile.objects.create(user=new_user, phone_number=phone_number)
        login(username, password)
        server_data['registered'] = True
    else:
        server_data['registered'] = False

    return JsonResponse(server_data)


def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_profile = user.userprofile
        server_data = {
            'user': user,
            'user_profile': user_profile,
        }
        return JsonResponse(server_data)
    except:
        return JsonResponse({})
