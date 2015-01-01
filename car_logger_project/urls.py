from django.conf.urls import patterns, include, url
from django.conf import settings
from logger.views import Login, Register, logout, Index, CarProfile, EntryDetial

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Index.as_view(), name='Index'),
    url(r'^login/', Login.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^cars/(?P<car_id>\d+)/$', CarProfile.as_view()),
    url(r'^entries/(?P<entry_id>\d+)/$', EntryDetial.as_view())
)

if settings.DEBUG:
    urlpatterns += patterns (
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )