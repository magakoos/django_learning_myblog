from django.conf.urls import patterns, url
from apps.blogeg import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.post, name='post'),
    url(r'^arhive/$', views.arhive, name='arhive')
)
