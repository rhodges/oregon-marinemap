# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EastOfTerritorialSeaLine'
        db.create_table('omm_manipulators_eastofterritorialsealine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=99999, null=True, blank=True)),
        ))
        db.send_create_signal('omm_manipulators', ['EastOfTerritorialSeaLine'])


    def backwards(self, orm):
        
        # Deleting model 'EastOfTerritorialSeaLine'
        db.delete_table('omm_manipulators_eastofterritorialsealine')


    models = {
        'omm_manipulators.eastofterritorialsealine': {
            'Meta': {'object_name': 'EastOfTerritorialSeaLine'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['omm_manipulators']
