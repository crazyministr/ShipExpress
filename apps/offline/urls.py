from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.offline.views',
    url(r'^$', 'offline_calculation', name='offline-calculation'),
)
