# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Cities'
        db.create_table('analysis_cities', (
            ('effectv_dt', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('gis_prc_dt', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=99999, null=True, blank=True)),
            ('fips_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('acres', self.gf('django.db.models.fields.FloatField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['Cities'])

        # Adding model 'Islands'
        db.create_table('analysis_islands', (
            ('perimeter', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('namenoaa', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('nwrname', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('area', self.gf('django.db.models.fields.FloatField')()),
            ('nwrunit', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('tractno', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('ifwsno', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('islandno', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('acreage', self.gf('django.db.models.fields.FloatField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=99999, null=True, blank=True)),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('org_bnd', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org_bnd_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('analysis', ['Islands'])

        # Adding model 'Ports'
        db.create_table('analysis_ports', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('harbor', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=99999, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['Ports'])

        # Adding model 'Counties'
        db.create_table('analysis_counties', (
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('objectid_1', self.gf('django.db.models.fields.IntegerField')()),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=99999, null=True, blank=True)),
            ('cobcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['Counties'])

        # Adding model 'Shoreline'
        db.create_table('analysis_shoreline', (
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('lpoly', self.gf('django.db.models.fields.FloatField')()),
            ('fnode_1', self.gf('django.db.models.fields.FloatField')()),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('esi_id', self.gf('django.db.models.fields.FloatField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(srid=99999, null=True, blank=True)),
            ('esi_field', self.gf('django.db.models.fields.FloatField')()),
            ('rpoly', self.gf('django.db.models.fields.FloatField')()),
            ('tnode', self.gf('django.db.models.fields.FloatField')()),
            ('lpoly_1', self.gf('django.db.models.fields.FloatField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('tnode_1', self.gf('django.db.models.fields.FloatField')()),
            ('esi_line_i', self.gf('django.db.models.fields.FloatField')()),
            ('esi', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rpoly_1', self.gf('django.db.models.fields.FloatField')()),
            ('source_id', self.gf('django.db.models.fields.FloatField')()),
            ('line', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('esi_line', self.gf('django.db.models.fields.FloatField')()),
            ('fnode', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('analysis', ['Shoreline'])

        # Adding model 'RockyShores'
        db.create_table('analysis_rockyshores', (
            ('pc', self.gf('django.db.models.fields.IntegerField')()),
            ('bm_cl', self.gf('django.db.models.fields.IntegerField')()),
            ('rec_u', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('bc', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=99999, null=True, blank=True)),
            ('visitor', self.gf('django.db.models.fields.IntegerField')()),
            ('ed_u', self.gf('django.db.models.fields.IntegerField')()),
            ('te_species', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.IntegerField')()),
            ('rsindx', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desig', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('com_u', self.gf('django.db.models.fields.IntegerField')()),
            ('it_cl', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('reg', self.gf('django.db.models.fields.FloatField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('analysis', ['RockyShores'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Cities'
        db.delete_table('analysis_cities')

        # Deleting model 'Islands'
        db.delete_table('analysis_islands')

        # Deleting model 'Ports'
        db.delete_table('analysis_ports')

        # Deleting model 'Counties'
        db.delete_table('analysis_counties')

        # Deleting model 'Shoreline'
        db.delete_table('analysis_shoreline')

        # Deleting model 'RockyShores'
        db.delete_table('analysis_rockyshores')
    
    
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
        'analysis.counties': {
            'Meta': {'object_name': 'Counties'},
            'cobcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'county_nam': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '99999', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'islandno': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'te_species': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
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
