# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NonConsumptive'
        db.create_table('non_consumptive_nonconsumptive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('kml', self.gf('django.db.models.fields.files.FileField')(max_length=510)),
        ))
        db.send_create_signal('non_consumptive', ['NonConsumptive'])


    def backwards(self, orm):
        
        # Deleting model 'NonConsumptive'
        db.delete_table('non_consumptive_nonconsumptive')


    models = {
        'non_consumptive.nonconsumptive': {
            'Meta': {'object_name': 'NonConsumptive'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kml': ('django.db.models.fields.files.FileField', [], {'max_length': '510'})
        }
    }

    complete_apps = ['non_consumptive']
