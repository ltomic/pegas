from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pegas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

		url(r'^paas/', include('lark.urls', namespace="lark")),
    url(r'^admin/', include(admin.site.urls)),
]
