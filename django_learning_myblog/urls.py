from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.blogeg import urls as blogeg_urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(blogeg_urls, namespace='blogeg')),
    url(r'^accounts/', include('apps.accounts.urls')),
)

