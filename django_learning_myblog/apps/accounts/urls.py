from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset as registration
from django.contrib.auth.views import password_reset_complete as registration_complete
from django.contrib.auth.views import password_reset_done as registration_done
from apps.accounts.forms import BlogegRegistrationForm
from apps.accounts.views import account
from apps.accounts.views import registration_confirm

UID = '(?P<uidb64>[0-9A-Za-z_\-]+)'
TOKEN = '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'

urlpatterns = patterns('',
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', account, name='account'),
    url(r'^registration_confirm/'+UID+'/'+TOKEN+'/$',
        registration_confirm,
        name='registration_confirm'
        ),
    url(r'^registration_comlete', registration_complete,
        {
        'template_name': 'registration/registration_complete.html'
        },
        name='registration_comlete'
        ),
        url(r'^registration_done', registration_done,
        {
        'template_name': 'registration/registration_done.html'
        },
        name='registration_done'
        ),    
    url(r'^registration', registration, 
        {
        'template_name': 'registration/registration.html',
        'email_template_name': 'registration/registration_email.html',
        'subject_template_name': 'registration/registration_subject.txt',
        'password_reset_form': BlogegRegistrationForm,
        'post_reset_redirect': 'registration_comlete'
        },
        name='registration'
        )
    
)