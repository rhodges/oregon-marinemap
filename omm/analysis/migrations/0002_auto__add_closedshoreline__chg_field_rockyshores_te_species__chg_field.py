# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ClosedShoreline'
        db.create_table('analysis_closedshoreline', (
            ('lpoly', self.gf('django.db.models.fields.IntegerField')()),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(srid=99999, null=True, blank=True)),
            ('rpoly', self.gf('django.db.models.fields.IntegerField')()),
            ('tnode', self.gf('django.db.models.fields.IntegerField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('esi_ln', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('esi_ln_id', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fnode', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('analysis', ['ClosedShoreline'])

        # Changing field 'RockyShores.te_species'
        db.alter_column('analysis_rockyshores', 'te_species', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True))

        # Changing field 'Islands.islandno'
        db.alter_column('analysis_islands', 'islandno', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting model 'ClosedShoreline'
        db.delete_table('analysis_closedshoreline')

        # Changing field 'RockyShores.te_species'
        db.alter_column('analysis_rockyshores', 'te_species', self.gf('django.db.models.fields.CharField')(max_length=12))

        # Changing field 'Islands.islandno'
        db.alter_column('analysis_islands', 'islandno', self.gf('django.db.models.fields.CharField')(max_length=10))
    
    
    models = {
        'analysis.cities': {
            'Meta': {'object_name': 'Cities'},
            'acres': ('django.db.models.fields.FloatField', [], {}),
            'effectv_dt': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'gis_prc_dt': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {})
        },
        'analysis.closedshoreline': {
            'Meta': {'object_name': 'ClosedShoreline'},
            'esi_ln': ('django.db.models.fields.IntegerField', [], {}),
            'esi_ln_id': ('django.db.models.fields.IntegerField', [], {}),
            'fnode': ('django.db.models.fields.IntegerField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'lpoly': ('django.db.models.fields.IntegerField', [], {}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'rpoly': ('django.db.models.fields.IntegerField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'tnode': ('django.db.models.fields.IntegerField', [], {})
        },
        'analysis.counties': {
            'Meta': {'object_name': 'Counties'},
            'cobcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'objectid_1': ('django.db.models.fields.IntegerField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {})
        },
        'analysis.islands': {
            'Meta': {'object_name': 'Islands'},
            'acreage': ('django.db.models.fields.FloatField', [], {}),
            'area': ('django.db.models.fields.FloatField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifwsno': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'islandno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'namenoaa': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'nwrname': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'nwrunit': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'org_bnd': ('django.db.models.fields.IntegerField', [], {}),
            'org_bnd_id': ('django.db.models.fields.IntegerField', [], {}),
            'perimeter': ('django.db.models.fields.FloatField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'tractno': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'analysis.ports': {
            'Meta': {'object_name': 'Ports'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'harbor': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {})
        },
        'analysis.rockyshores': {
            'Meta': {'object_name': 'RockyShores'},
            'bc': ('django.db.models.fields.IntegerField', [], {}),
            'bm_cl': ('django.db.models.fields.IntegerField', [], {}),
            'com_u': ('django.db.models.fields.IntegerField', [], {}),
            'desig': ('django.db.models.fields.IntegerField', [], {}),
            'ed_u': ('django.db.models.fields.IntegerField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it_cl': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'pc': ('django.db.models.fields.IntegerField', [], {}),
            'rec_u': ('django.db.models.fields.IntegerField', [], {}),
            'reg': ('django.db.models.fields.FloatField', [], {}),
            'rsindx': ('django.db.models.fields.IntegerField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'site': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'te_species': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'visitor': ('django.db.models.fields.IntegerField', [], {})
        },
        'analysis.shoreline': {
            'Meta': {'object_name': 'Shoreline'},
            'esi': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'esi_field': ('django.db.models.fields.FloatField', [], {}),
            'esi_id': ('django.db.models.fields.FloatField', [], {}),
            'esi_line': ('django.db.models.fields.FloatField', [], {}),
            'esi_line_i': ('django.db.models.fields.FloatField', [], {}),
            'fnode': ('django.db.models.fields.FloatField', [], {}),
            'fnode_1': ('django.db.models.fields.FloatField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'line': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'lpoly': ('django.db.models.fields.FloatField', [], {}),
            'lpoly_1': ('django.db.models.fields.FloatField', [], {}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'rpoly': ('django.db.models.fields.FloatField', [], {}),
            'rpoly_1': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'source_id': ('django.db.models.fields.FloatField', [], {}),
            'tnode': ('django.db.models.fields.FloatField', [], {}),
            'tnode_1': ('django.db.models.fields.FloatField', [], {})
        }
    }
    
    complete_apps = ['analysis']
