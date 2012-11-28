# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Floor.id_edificio'
        db.delete_column('buildings_floor', 'id_edificio_id')

        # Adding field 'Floor.building'
        db.add_column('buildings_floor', 'building',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Building']),
                      keep_default=False)

        # Adding field 'Room.building'
        db.add_column('buildings_room', 'building',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Building']),
                      keep_default=False)

        # Adding field 'Point.building'
        db.add_column('buildings_point', 'building',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Building']),
                      keep_default=False)

        # Deleting field 'Path.piano'
        db.delete_column('buildings_path', 'piano_id')

        # Adding field 'Path.building'
        db.add_column('buildings_path', 'building',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Building']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Floor.id_edificio'
        db.add_column('buildings_floor', 'id_edificio',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Building']),
                      keep_default=False)

        # Deleting field 'Floor.building'
        db.delete_column('buildings_floor', 'building_id')

        # Deleting field 'Room.building'
        db.delete_column('buildings_room', 'building_id')

        # Deleting field 'Point.building'
        db.delete_column('buildings_point', 'building_id')

        # Adding field 'Path.piano'
        db.add_column('buildings_path', 'piano',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['buildings.Floor']),
                      keep_default=False)

        # Deleting field 'Path.building'
        db.delete_column('buildings_path', 'building_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'data_creazione': ('django.db.models.fields.DateTimeField', [], {}),
            'data_update': ('django.db.models.fields.DateTimeField', [], {}),
            'descrizione': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'geometria': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'numero_di_piani': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'posizione': ('django.contrib.gis.db.models.fields.PointField', [], {'unique': 'True', 'null': 'True'}),
            'pronto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'versione': ('django.db.models.fields.IntegerField', [], {})
        },
        'buildings.floor': {
            'Meta': {'object_name': 'Floor'},
            'bearing': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'descrizione': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'immagine': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'numero_di_piano': ('django.db.models.fields.IntegerField', [], {}),
            'posizione_immagine': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'zoom_on_map': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'})
        },
        'buildings.path': {
            'Meta': {'object_name': 'Path'},
            'a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'path_A'", 'to': "orm['buildings.Point']"}),
            'ascensore': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'path_B'", 'to': "orm['buildings.Point']"}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scala': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'buildings.point': {
            'Meta': {'object_name': 'Point'},
            'RFID': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingresso': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'piano': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Floor']"}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        'buildings.room': {
            'Meta': {'object_name': 'Room'},
            'altro': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'nome_stanza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'punto': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['buildings.Point']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['buildings']