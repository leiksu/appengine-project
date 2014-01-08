from django.conf.urls import *
from django.conf import settings
from core import views

urlpatterns = patterns('',
    url(r'^$', views.hello_world, name='hello-world'),
    url(r'^blog$', views.view_blog),
    url(r'^delete/(\d+)/$',views.delete_blog),
    url(r'^create$',views.create_blog),
    url(r'^edit/(\d+)/$',views.create_blog),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )
