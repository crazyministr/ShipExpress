from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.installation.views',

    url(r'^ports/$', 'ports_page_view', name='ports-page-view'),
    url(r'^ports/(?P<sid>\d+)/$', 'port_page_view', name='port-page',
        kwargs={'url': 'ports'}),
    url(r'^ports/(?P<sid>\d+)/(?P<action>\w+)/$', 'port_page_view', name='port-page-action',
        kwargs={'url': 'ports'}),

    url(r'^ships/$', 'ships_page_view', name='ships-page-view'),
    url(r'^ships/(?P<sid>\d+)/$', 'ship_page_view', name='ship-page',
        kwargs={'url': 'ships'}),
    url(r'^ships/(?P<sid>\d+)/(?P<action>\w+)/$', 'ship_page_view', name='ship-page-action',
        kwargs={'url': 'ships'}),

    url(r'^icebreakers/$', 'icebreakers_page_view', name='icebreakers-page-view'),
    url(r'^icebreakers/(?P<sid>\d+)/$', 'icebreaker_page_view', name='icebreaker-page',
        kwargs={'url': 'icebreakers'}),
    url(r'^icebreakers/(?P<sid>\d+)/(?P<action>\w+)/$', 'icebreaker_page_view', name='icebreaker-page-action',
        kwargs={'url': 'icebreakers'}),

    url(r'^equipments/$', 'equipments_page_view', name='equipments-page-view'),
    url(r'^equipments/(?P<sid>\d+)/$', 'equipment_page_view', name='equipment-page',
        kwargs={'url': 'equipments'}),
    url(r'^equipments/(?P<sid>\d+)/(?P<action>\w+)/$', 'equipment_page_view', name='equipment-page-action',
        kwargs={'url': 'equipments'}),
)
