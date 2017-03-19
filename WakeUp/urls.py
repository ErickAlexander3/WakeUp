"""
Definition of urls for WakeUp.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.scheduler
import app.ajax as ajax_views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^permission/$', app.scheduler.getPermission, name = 'permission'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    #login and registration
    url(r'^login_or_register/$', ajax_views.login_or_register, name='login_or_register'),
    url(r'^register/$', ajax_views.register, name='register'),
    url(r'^user/(?P<user_id>\d+)$', ajax_views.get_user, name='get_user'),
    #main screen
    url(r'main/$', app.views.main, name='main'),
    #schedule alarm
    url(r'schedule_alarm/$', app.views.schedule_alarm, name='schedule_alarm'),
    #active section
    url(r'active/$', app.views.active, name='active'),
    #final call
    url(r'call/$', app.views.call, name='call'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
