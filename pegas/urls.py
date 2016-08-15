from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pegas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('lark.urls', namespace='lark')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^', include('tasks.urls', namespace='tasks')),
    url(r'^admin/', include(admin.site.urls)),
]
