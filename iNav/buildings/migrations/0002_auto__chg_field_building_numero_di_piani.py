# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Building.numero_di_piani'
        db.alter_column('buildings_building', 'numero_di_piani', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Building.numero_di_piani'
        raise RuntimeError("Cannot reverse this migration. 'Building.numero_di_piani' and its values cannot be restored.")

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
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'numero_di_piani': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'posizione': ('django.contrib.gis.db.models.fields.PointField', [], {'unique': 'True', 'null': 'True'}),
            'pronto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'versione': ('django.db.models.fields.IntegerField', [], {})
        },
        'buildings.floor': {
            'Meta': {'object_name': 'Floor'},
            'bearing': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'descrizione': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_edificio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'immagine': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'numero_di_piano': ('django.db.models.fields.IntegerField', [], {}),
            'posizione_immagine': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'zoom_on_map': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'})
        },
        'buildings.path': {
            'Meta': {'object_name': 'Path'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_edificio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'numero_di_piano': ('django.db.models.fields.IntegerField', [], {}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'x1': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {}),
            'y1': ('django.db.models.fields.IntegerField', [], {})
        },
        'buildings.point': {
            'Meta': {'object_name': 'Point'},
            'RFID': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ascensore': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_edificio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'ingresso': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numero_di_piano': ('django.db.models.fields.IntegerField', [], {}),
            'scala': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'stanza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        'buildings.room': {
            'Meta': {'object_name': 'Room'},
            'altro': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_edificio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buildings.Building']"}),
            'id_punto': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['buildings.Point']", 'unique': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'nome_stanza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
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