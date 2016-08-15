from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^search_task/$', views.search_task, name='search_task'),
        )
