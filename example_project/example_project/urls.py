from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^geoprisma/', include("geoprisma.urls", namespace="geoprisma")),
    url(r'^map/(?P<wsName>[\w-]+)/(?P<viewId>[\w-]+)$', 'example_project.views.maprender'),
)
