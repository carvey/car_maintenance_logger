from django.conf.urls import patterns, include, url
from django.conf import settings
from logger.views import Login, Register, logout, Index, CarProfile, EntryDetial, add_car, add_entry

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Index.as_view(), name='Index'),
    url(r'^login/', Login.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^cars/(?P<car_id>\d+)/$', CarProfile.as_view(), name="car_profile"),
    url(r'^cars/add/$', add_car, name='add_car'),
    url(r'^entries/(?P<entry_id>\d+)/$', EntryDetial.as_view()),
    url(r'^entries/add/(?P<car_id>\d+)/$', add_entry, name='add_entry'),
    )

if settings.DEBUG:
    urlpatterns += patterns (
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )