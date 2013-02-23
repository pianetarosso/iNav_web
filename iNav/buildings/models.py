# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from sorl.thumbnail import ImageField
import datetime
import os


def content_file_name(instance, filename):
                
        estensione = '.jpg'
                
        posizione_punto = filename.rfind('.')
                
        if posizione_punto > 0:
                estensione = filename[posizione_punto:]
                
        now = datetime.datetime.now()
        print str(instance.utente)
        
        return '/'.join(['buildings', str(instance.utente.pk), str(now) + estensione])
                
    
class Building(models.Model):

        # Utente creatore dell'edificio
        utente = models.ForeignKey(User);
        
        # in pratica toString()
        def __unicode__(self):
                return self.nome
         
       
       
        
        # caratteristiche dell'edificio (PUNTO 1)
        nome = models.CharField(max_length=200, unique=True)
        descrizione = models.TextField(max_length=1000, blank=True)
        link = models.URLField(blank=True)
        
        
        
        foto = ImageField(upload_to=content_file_name, blank=True)
        
        
        # Geo Django (PUNTO 2):
        posizione = models.PointField(help_text="POINT(longitude latitude)", unique=True, srid=4326, null=True, blank=True)
        geometria = models.PolygonField(help_text="POLYGON((longitude latitude, ..))", srid=4326, null=True, blank=True, geography=True)
        
        # Necessario per le geoquery
        objects = models.GeoManager() 
        
        
        # Dati sulla posizione (usati nella ricerca)
        nazione = models.CharField(max_length=30, blank=True)
        citta = models.CharField(max_length=30, blank=True)

        
        
        # dati interni dell'applicazione points
        versione = models.IntegerField() 
        data_creazione = models.DateTimeField('data creazione')
        data_update = models.DateTimeField('data update')
        
        # indica che il building è pronto per la visualizzazione
        pronto = models.BooleanField() 
        
           
        
                
class Floor(models.Model):
    
          
        # edificio di riferimento
        building = models.ForeignKey(Building)
        
        # dati vari del piano   
        numero_di_piano = models.IntegerField()
        descrizione = models.TextField(max_length=1000, blank=True)
        bearing = models.DecimalField(max_digits=6, decimal_places=2, null=True)
        immagine = ImageField(upload_to=content_file_name)
            
        # valori per rappresentare l'immagine del piano sulla mappa
        zoom_on_map = models.DecimalField(max_digits=5, decimal_places=3, null=True)
        posizione_immagine = models.PointField(help_text="POINT(longitude latitude)", null=True, srid=4326)
        




 # modificare per usare class PointField 
class Point(models.Model):

        # edificio di riferimento
        building = models.ForeignKey(Building)
        
        # piano su cui si trova il punto
        piano = models.ForeignKey(Floor)
        
        # RFID
        RFID = models.CharField(max_length=200, blank=True)
        
        # posizione dei punti sull'immagine
        x = models.IntegerField()
        y = models.IntegerField()
        
        # valore booleano che indica se quello è un ingresso
        ingresso = models.BooleanField()
       
          
    
class Room(models.Model):
            
        # edificio di riferimento
        building = models.ForeignKey(Building)
        
        # punto di riferimento
        punto = models.OneToOneField(Point)
            
        # altri parametri descrittivi
        nome_stanza = models.CharField(max_length=200, blank=True)
        persone = models.CharField(max_length=200, blank=True)
        altro = models.CharField(max_length=200, blank=True)
        link = models.URLField(blank=True)
            
        def __unicode__(self):
                return self.nome_stanza    
    
# modificare con class MultiLineStringField per contenere tutte le path di un piano in un solo oggetto
class Path(models.Model):

        # edificio di riferimento
        building = models.ForeignKey(Building)
        
        # punto di partenza
        a = models.ForeignKey(Point, related_name='path_A')
        
        # punto di arrivo
        b = models.ForeignKey(Point, related_name='path_B')
        
        # valori di ascensore/scala, usati per dare migliori indicazioni e 
        # aiutare la computazione dei percorsi (vengono usati anche come indicatori booleani)
        ascensore  = models.CharField(max_length=50, blank=True)
        scala  = models.CharField(max_length=50, blank=True)
        
  
# personalizzazione del User di default di django
from django.db.models.signals import *
        
class UserAdditionalFields(models.Model):

        user = models.OneToOneField(User)
        
        # valore che indica il numero di edifici incompleti per ogni utenti 
        incomplete_buildings = models.IntegerField(null=False, default=0)
        
        # valore che indica gli edifici creati da ogni utente
        complete_buildings = models.IntegerField(null=False, default=0)
       
         # necessario per il salvataggio dell'utente
        def create_user_profile(sender, instance, created, **kwargs):
                if created:
                        UserAdditionalFields.objects.create(user=instance)
                        
        post_save.connect(create_user_profile, sender=User)
        
    
