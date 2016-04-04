from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.calculation.views',
    url(r'^calculation/yandex-maps/$', 'ymaps_calculation_page_view',
        name='yandex-calculation-page-view'),
    url(r'^calculation/google-maps/$', 'google_calculation_page_view',
        name='google-calculation-page-view'),
    url(r'^ajax_calculation/$', 'calculation_view', name='calculation-view'),
)
