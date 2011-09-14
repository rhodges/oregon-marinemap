# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'PublicFishingLayer'
        db.create_table('fishing_layers_publicfishinglayer', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('kml', self.gf('django.db.models.fields.files.FileField')(max_length=510)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('fishing_layers', ['PublicFishingLayer'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'PublicFishingLayer'
        db.delete_table('fishing_layers_publicfishinglayer')
    
    
    models = {
        'fishing_layers.publicfishinglayer': {
            'Meta': {'object_name': 'PublicFishingLayer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kml': ('django.db.models.fields.files.FileField', [], {'max_length': '510'})
        }
    }
    
    complete_apps = ['fishing_layers']
