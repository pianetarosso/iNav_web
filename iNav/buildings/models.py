from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
import os


    
class Building(models.Model):

        # Utente creatore dell'edificio
        utente = models.ForeignKey(User);
        
        # in pratica toString()
        def __unicode__(self):
                return self.nome
         
           
       # def content_file_name(instance, filename):
       #         fileName, fileExtension = os.path.splitext(filename)
       #         return '/'.join(['buildings', instance.utente.id + '_%Y-%m-%d'+fileExtension])
                
       # foto = models.ImageField(upload_to=content_file_name, blank=True)
       
       
        
        # caratteristiche dell'edificio
        nome = models.CharField(max_length=200, unique=True)
        descrizione = models.TextField(max_length=1000, blank=True)
        link = models.URLField(blank=True)
        numero_di_piani = models.IntegerField(null=True)
        foto = models.ImageField(upload_to='buildings', blank=True)
        
        # dati interni dell'applicazione
        versione = models.IntegerField() 
        data_creazione = models.DateTimeField('data creazione')
        data_update = models.DateTimeField('data update')
        pronto = models.BooleanField() # indica che il building e' pronto per la visualizzazione
        
        # Geo Django:
        posizione = models.PointField(help_text="POINT(longitude latitude)", unique=True, srid=4326, null=True)
        geometria = models.PolygonField(help_text="POLYGON((longitude latitude ..))", srid=4326, null=True)

        # Necessario per le geoquery
        objects = models.GeoManager()     
        
                
class Floor(models.Model):
    
   # def content_file_name(instance, filename):
   #             fileName, fileExtension = os.path.splitext(filename)
   #             return '/'.join(['floors', instance.id_edificio.utente.id + '_%Y-%m-%d'+fileExtension])
   #             
   # link = models.ImageField(upload_to=content_file_name, blank=True)
        
        # edificio di riferimento
        id_edificio = models.ForeignKey(Building)
        
        # dati vari del piano
        immagine = models.ImageField(upload_to='floors')
        numero_di_piano = models.IntegerField()
        descrizione = models.TextField(max_length=1000, blank=True)
        bearing = models.DecimalField(max_digits=6, decimal_places=2, null=True)
            
        # valori per rappresentare l'immagine del piano sulla mappa
        zoom_on_map = models.DecimalField(max_digits=5, decimal_places=3, null=True)
        posizione_immagine = models.PointField(help_text="POINT(longitude latitude)", null=True, srid=4326)

 # modificare per usare class PointField (verificare qual'e' il migliore srid)  
class Point(models.Model):

        # RFID
        RFID = models.CharField(max_length=200, blank=True)
        
        # posizione dei punti sull'immagine
        x = models.IntegerField()
        y = models.IntegerField()
        
        # piano su cui si trova il punto
        piano = models.ForeignKey(Floor)
        
        # valore booleano che indica se quello e' un ingresso
        ingresso = models.BooleanField()
       
          
    
class Room(models.Model):
            
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

        # piano su cui si trova il percorso
        piano = models.ForeignKey(Floor)
        
        # punto di partenza
        a = models.ForeignKey(Point, related_name='path_A')
        
        # punto di arrivo
        b = models.ForeignKey(Point, related_name='path_B')
        
        # valori di ascensore/scala, usati per dare migliori indicazioni e 
        # aiutare la computazione dei percorsi (vengono usati anche come indicatori booleani)
        ascensore  = models.CharField(max_length=50, blank=True)
        scala  = models.CharField(max_length=50, blank=True)
        
    
   
    
    
