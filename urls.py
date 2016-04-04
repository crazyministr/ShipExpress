from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('apps.offline.urls', namespace='home')),
    (r'^', include('apps.installation.urls', namespace='installation')),
    (r'^', include('apps.calculation.urls', namespace='calculation')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
