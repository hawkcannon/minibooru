from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^view/(?P<post_id>[0-9]+)/$', 'my_booru.views.viewPost'),
	url(r'^post/$', 'my_booru.views.makePost'),
	url(r'^search/$', 'my_booru.views.searchByTags'),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'mybooru.views.home', name='home'),
    # url(r'^mybooru/', include('mybooru.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
