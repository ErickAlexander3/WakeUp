
from app.models import UserProfile, CallRequest
import datetime
from django.db.models.aggregates import Max, Min
from django.core import serializers
from django.http import JsonResponse
import math



def getUserPriorities():
    """ Returns a list of userIDs for all active users in order of their priority"""

    activeUsers = UserProfile.entries.filter(active = True)

    scoreTracker = {}
    annotated_users = activeUsers.annotate(most_recent_call=Max('completed_requests__time_of_call'))
    for user in activeUsers: 
        #mostRecentCompletion = user.completedRequests.aggregate(Max('time_of_call'))['time_of_call__max']
        mostRecentCompletition = user.most_recent_call
        priorityScore = (datetime.datetime.now() - mostRecentCompletion).totalSeconds*user.callFreq
        scoreTracker[priorityScore] = user

    for score in sorted(scoreTracker.keys(),reversed = True):
        priorityList.append(scoreTracker[score].id)

    return priorityList

def getBestRequest():
    """Return the highest priority request in a JSON serialized format"""


    earliestDeadline = activeRequests.aggregate(Min(time_of_call))[time_of_call__max]
    bestRequest = activeRequests.get(time_of_call = earliestDeadline)

    return bestRequest

def getPermission(request):
    user_id = request.POST.get('user_id')
    
    priorityList = getUserPriorities(UserProfile.entries.filter(active=True))

    #if this user is in the top 20% of user priority
    if user_id in priorityList[:math.floor(len(priorityList)/5)]:
        approvedRequest = getBestRequest()
        user = UserProfile.entries.get(user_id = user_id)
        data = {'permission_status' :True,
                'description'       :user.description,
                'requestee_number'  :approvedRequest.requestee.phone_number,
                'request_id'        :approvedRequest.id}

        #flag that this request has been passed to the user
        approvedRequest.is_pending = True
        approvedRequest.save()      
    else:
        data = {'permission_status': False}
    return JsonResponse(data)




