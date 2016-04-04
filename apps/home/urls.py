from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.home.views',
    url(r'^$', 'home', name='home-page'),
)
