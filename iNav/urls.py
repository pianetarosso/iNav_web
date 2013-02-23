# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url


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

        # Avatar
        (r'^avatar/', include('avatar.urls')),
            
        # vetrina dell'applicazione (da creare)
        url(r'^buildings/iNav/$', 'buildings.views.show'),
        
        # index
        url(r'^buildings/$', 'buildings.views.index'),
        
        # visualizzazione degli edifici creati più recentemente 
        url(r'^buildings/update_list', 'buildings.views.update_list'),
        
        # recupero un edificio in base all'id, o di una lista di edifici in base alla posizione
        url(r'^buildings/get/building=(?P<id_>-?\d+)&(?P<latitude>-?\d+\.\d+)&(?P<longitude>-?\d+\.\d+)&(?P<radius>\d+)', 'buildings.views.getBuildings'), 
        
        # recupero i piani di un edificio (usato nel wizard)
        url(r'^buildings/get/floor&(?P<building_id>\d+)', 'buildings.views.getFloors'),   
        
        # cancellazione di un edificio in base all'id
        url(r'^buildings/delete=(?P<b_id>\d+)', 'buildings.views.delete'),   
        
        
        # generazione building
        #url(r'^buildings/generate/list, 'buildings.views.list_incomplete'),
        #url(r'^buildings/generate/new_building=(?P<new_id>-?\d+)', 'buildings.views.generate'),
        
        url(r'^buildings/generate/new_building=(?P<idb>-?\d+)', 'buildings.views.generate_building'),
        #url(r'^buildings/generate/step=(?P<new_id>\d+)', 'buildings.views.step'),
        
        
        
        
        
        
        
        
        
        # dettagli di un edificio e lista dei propri edifici
        url(r'^buildings/(?P<building_id>\d+)/$', 'buildings.views.detail'),
        url(r'^buildings/my_buildings', 'buildings.views.my_buildings'),
        
        
            
            
            
        # generazione di immagini ridimensionate (serve?)
        url(r'^buildings/generate/image_r(?P<idf>\d+)&(?P<id_b>\d+)&(?P<width>\d+)', 'buildings.views.setBearingimage'),

        
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
