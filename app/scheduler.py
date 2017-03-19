
from app.models import UserProfile, CallRequest
from django.contrib.auth.models import User

import datetime
from django.db.models.aggregates import Min
from django.db.models import Max
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
import math

def getUserPriorities():
    """ Returns a list of userIDs for all active users in order of their priority"""

    activeUsers = UserProfile.objects.filter(active = True)
 
    scoreTracker = {}
    annotated_users = activeUsers.annotate(most_recent_call=Max('user__completed_requests__time_of_call'))
    for user in annotated_users: 
        #mostRecentCompletion = user.completedRequests.aggregate(Max('time_of_call'))['time_of_call__max']
        mostRecentCompletition = user.most_recent_call
        if mostRecentCompletition:
            priorityScore = (datetime.datetime.now() - mostRecentCompletition).totalSeconds
        else:
            priorityScore = 9999
        scoreTracker[priorityScore] = user

    priorityList = []
    for score in sorted(scoreTracker.keys(),reverse = True):
        priorityList.append(scoreTracker[score].id)

    return priorityList

def getBestRequest(user_id):
    """Return the highest priority request in a JSON serialized format"""
    activeRequests = CallRequest.objects.filter(~Q(requestee_id=user_id), is_completed=False, is_pending=False, time_of_call__lte= datetime.datetime.now() + datetime.timedelta(minutes=5))
    earliestDeadline = activeRequests.aggregate(Min('time_of_call'))['time_of_call__min']
    try:
        print(earliestDeadline)
        bestRequest = activeRequests.get(time_of_call = earliestDeadline)
    except:
        bestRequest = None
    return bestRequest

def getPermission(request):
    user_id = request.POST.get('user_id')
    priorityList = getUserPriorities()
    #if this user is in the top 20% of user priority
    if int(user_id) == priorityList[0]:
        print('this should be happening')
        approvedRequest = getBestRequest(user_id)
        print(approvedRequest)
        print(user_id)
        user = User.objects.get(id = user_id).userprofile
        if approvedRequest:
            print('this should also be happening')
            data = {'permission_status' :True,
                    'description'       :approvedRequest.description,
                    'requestee_number'  :approvedRequest.requestee.userprofile.phone_number,
                    'request_id'        :approvedRequest.id}
            #flag that this request has been passed to the user and flag the user as inactive
            user.active = False
            user.save()
            approvedRequest.is_pending = True
            approvedRequest.save() 
        else:
            data = {'permission_status': False}
    else:
        data = {'permission_status': False}
    return JsonResponse(data)




