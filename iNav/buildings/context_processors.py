# -*- coding: utf-8 -*-

from django.conf import settings


def constants(request):
        
        return {
                # Area massima e minima della geometria (m^2)
                'MAX_GEOMETRY_AREA'   :       settings.MAX_GEOMETRY_AREA,
                'MIN_GEOMETRY_AREA'   :       settings.MIN_GEOMETRY_AREA,
                
                # Lunghezza massima e minima di un lato della geometria
                'MAX_GEOMETRY_LENGTH'   :       settings.MAX_GEOMETRY_LENGTH,
                'MIN_GEOMETRY_LENGTH'   :       settings.MIN_GEOMETRY_LENGTH,
                
                # Dimensione massima delle immagini in input (Mb)
                'MAX_IMAGE_SIZE'        :       settings.MAX_IMAGE_SIZE,
                
                # Numero massimo di piani mappabili in un colpo
                'MAX_FLOORS'            :       settings.MAX_FLOORS,
                
                # Chiave Google Maps
                'G_MAPS'                :      settings.G_MAPS
                }
