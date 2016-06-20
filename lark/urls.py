from django.conf.urls import patterns, url
from lark import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^search_task/$', views.search_task, name='search_task'),
		url(r'^list_submissions/$', views.list_submissions, name='list_submissions'),
		url(r'^list_test_result', views.list_test_result, name='list_test_result'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^myuser/$', views.my_user, name='my_user'),
		url(r'^task/(?P<task_url>[\w]+)/$', views.detail, name='detail'),
		url(r'^task/(?P<task_url>[\w]+)/submit/$', views.submit, name='submit'),
		url(r'^task/(?P<task>[\w]+)/(?P<sub_id>[\w]+)/$', views.submission, name='submission'),
		)
