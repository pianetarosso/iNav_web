from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from buildings.models import *
from django.conf import settings
from django import forms
from django.views.generic.simple import direct_to_template
import allauth


admin.autodiscover()
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Point)
admin.site.register(Room)
admin.site.register(Path)

    
urlpatterns = patterns('',
   
        # Admin 
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
            
        # Users
        (r'^accounts/', include('allauth.urls')),
        url(r'^accounts/profile/', 'buildings.views.profile'),

        # Avatar
        (r'^avatar/', include('avatar.urls')),
            
        # index
        url(r'^buildings/$', 'buildings.views.index'),
        
        # details
        url(r'^buildings/(?P<building_id>\d+)/$', 'buildings.views.detail'),
        url(r'^buildings/my_buildings', 'buildings.views.my_buildings'),
        
        # generazione building
        url(r'^buildings/generate/new_building=(?P<new_id>-?\d+)', 'buildings.views.generate'),
        url(r'^buildings/generate/step=(?P<new_id>\d+)', 'buildings.views.step'),
            
        # generazione di immagini ridimensionate
        url(r'^buildings/generate/image_r(?P<idf>\d+)&(?P<id_b>\d+)&(?P<width>\d+)', 'buildings.views.setBearingimage'),

        # visualizzazione degli edifici creati piu' recentemente nell'iFrame
        url(r'^buildings/iframe', 'buildings.views.iframe'),
        
        # recupero i dati (no csrf)
        #  url(r'^buildings/get/building(?P<id>\d+)&(?P<latitude>\d+)&(?P<longitude>\d+)&(?P<radius>\d+)', 'buildings.views.getBuildings'), 
        url(r'^buildings/get/floor&(?P<building_id>\d+)', 'buildings.views.getFloors'),   
        #    url(r'^buildings/get/point&(?P<building_id>\d+)', 'buildings.views.getPoints'),
        #    url(r'^buildings/get/path&(?P<building_id>\d+)', 'buildings.views.getPaths'),

)

if settings.DEBUG:
        # static files (images, css, javascript, etc.)
        urlpatterns += patterns('',
                (
                        r'^media/(?P<path>.*)$', 
                        'django.views.static.serve', 
                        {'document_root': settings.MEDIA_ROOT}
                )
        )
