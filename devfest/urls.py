from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .utilities import AppInitialization

from devfest import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Pattern examples:
# url(r'^$', 'devfest.views.home', name='home')
# url(r'^devfest/', include('devfest.foo.urls'))
urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.index', name='index'),    # Root url for application
    url(r'^test', views.test, name='test'),
    url(r'^game/', include('game.urls')),
    url(r'^account/', include('account.urls')),
    # Static content goes under the '/site_media/' directory
    # url (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

# Populate initial data
AppInitialization.initialize_database()