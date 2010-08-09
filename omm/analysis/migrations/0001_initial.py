# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'OregonPorts'
        db.create_table('analysis_oregonports', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('objectid', self.gf('django.db.models.fields.IntegerField')(db_column='OBJECTID')),
            ('harbor', self.gf('django.db.models.fields.CharField')(max_length=5, db_column='Harbor')),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=35, db_column='COUNTY')),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=2992, null=True, blank=True)),
            ('gid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['OregonPorts'])

        # Adding model 'Counties'
        db.create_table('analysis_counties', (
            ('shape_area', self.gf('django.db.models.fields.FloatField')(db_column='Shape_Area')),
            ('objectid_1', self.gf('django.db.models.fields.IntegerField')(db_column='OBJECTID_1')),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(srid=2992, null=True, blank=True)),
            ('cobcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')(db_column='Shape_Leng')),
            ('county_nam', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['Counties'])

        # Adding model 'Islands'
        db.create_table('analysis_islands', (
            ('perimeter', self.gf('django.db.models.fields.FloatField')(db_column='PERIMETER')),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5, db_column='STATUS')),
            ('nwrname', self.gf('django.db.models.fields.CharField')(max_length=3, db_column='NWRNAME')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='NameNOAA')),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('area', self.gf('django.db.models.fields.FloatField')(db_column='AREA')),
            ('nwrunit', self.gf('django.db.models.fields.CharField')(max_length=3, db_column='NWRUNIT')),
            ('tractno', self.gf('django.db.models.fields.CharField')(max_length=15, db_column='TRACTNO')),
            ('ifwsno', self.gf('django.db.models.fields.CharField')(max_length=5, db_column='IFWSNO')),
            ('islandno', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='ISLANDNO')),
            ('org_bnd_field', self.gf('django.db.models.fields.IntegerField')(db_column='ORG_BND_')),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(srid=2992, null=True, blank=True)),
            ('shape_area', self.gf('django.db.models.fields.FloatField')(db_column='Shape_Area')),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')(db_column='Shape_Leng')),
            ('acreage', self.gf('django.db.models.fields.FloatField')(db_column='ACREAGE')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org_bnd_id', self.gf('django.db.models.fields.IntegerField')(db_column='ORG_BND_ID')),
        ))
        db.send_create_signal('analysis', ['Islands'])

        # Adding model 'RockyShores'
        db.create_table('analysis_rockyshores', (
            ('bm_cl', self.gf('django.db.models.fields.IntegerField')()),
            ('rec_u', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('bc', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(srid=2992, null=True, blank=True)),
            ('visitor', self.gf('django.db.models.fields.IntegerField')()),
            ('ed_u', self.gf('django.db.models.fields.IntegerField')()),
            ('te_species', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('site', self.gf('django.db.models.fields.IntegerField')()),
            ('rsindx', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size_field', self.gf('django.db.models.fields.IntegerField')()),
            ('desig', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('com_u', self.gf('django.db.models.fields.IntegerField')()),
            ('it_cl', self.gf('django.db.models.fields.IntegerField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('reg', self.gf('django.db.models.fields.FloatField')()),
            ('pc', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('analysis', ['RockyShores'])

        # Adding model 'Cities'
        db.create_table('analysis_cities', (
            ('effectv_dt', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('gis_prc_dt', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=2992, null=True, blank=True)),
            ('fips_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('acres', self.gf('django.db.models.fields.FloatField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('city_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('analysis', ['Cities'])

        # Adding model 'Shoreline'
        db.create_table('analysis_shoreline', (
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('tnode_1', self.gf('django.db.models.fields.FloatField')()),
            ('fnode_field', self.gf('django.db.models.fields.FloatField')()),
            ('tnode_field', self.gf('django.db.models.fields.FloatField')()),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('esi_id', self.gf('django.db.models.fields.FloatField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(srid=2992, null=True, blank=True)),
            ('esi_field', self.gf('django.db.models.fields.FloatField')()),
            ('esi_line_field', self.gf('django.db.models.fields.FloatField')()),
            ('lpoly_1', self.gf('django.db.models.fields.FloatField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('rpoly_1', self.gf('django.db.models.fields.FloatField')()),
            ('esi_line_i', self.gf('django.db.models.fields.FloatField')()),
            ('source_id', self.gf('django.db.models.fields.FloatField')()),
            ('rpoly_field', self.gf('django.db.models.fields.FloatField')()),
            ('lpoly_field', self.gf('django.db.models.fields.FloatField')()),
            ('line', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('esi', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('fnode_1', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('analysis', ['Shoreline'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'OregonPorts'
        db.delete_table('analysis_oregonports')

        # Deleting model 'Counties'
        db.delete_table('analysis_counties')

        # Deleting model 'Islands'
        db.delete_table('analysis_islands')

        # Deleting model 'RockyShores'
        db.delete_table('analysis_rockyshores')

        # Deleting model 'Cities'
        db.delete_table('analysis_cities')

        # Deleting model 'Shoreline'
        db.delete_table('analysis_shoreline')
    
    
    models = {
        'analysis.cities': {
            'Meta': {'object_name': 'Cities'},
            'acres': ('django.db.models.fields.FloatField', [], {}),
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'effectv_dt': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
            'gis_prc_dt': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {})
        },
        'analysis.counties': {
            'Meta': {'object_name': 'Counties'},
            'cobcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'county_nam': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'objectid_1': ('django.db.models.fields.IntegerField', [], {'db_column': "'OBJECTID_1'"}),
            'shape_area': ('django.db.models.fields.FloatField', [], {'db_column': "'Shape_Area'"}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {'db_column': "'Shape_Leng'"})
        },
        'analysis.islands': {
            'Meta': {'object_name': 'Islands'},
            'acreage': ('django.db.models.fields.FloatField', [], {'db_column': "'ACREAGE'"}),
            'area': ('django.db.models.fields.FloatField', [], {'db_column': "'AREA'"}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifwsno': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_column': "'IFWSNO'"}),
            'islandno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ISLANDNO'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'NameNOAA'"}),
            'nwrname': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "'NWRNAME'"}),
            'nwrunit': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "'NWRUNIT'"}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'org_bnd_field': ('django.db.models.fields.IntegerField', [], {'db_column': "'ORG_BND_'"}),
            'org_bnd_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'ORG_BND_ID'"}),
            'perimeter': ('django.db.models.fields.FloatField', [], {'db_column': "'PERIMETER'"}),
            'shape_area': ('django.db.models.fields.FloatField', [], {'db_column': "'Shape_Area'"}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {'db_column': "'Shape_Leng'"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_column': "'STATUS'"}),
            'tractno': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_column': "'TRACTNO'"})
        },
        'analysis.oregonports': {
            'Meta': {'object_name': 'OregonPorts'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_column': "'COUNTY'"}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'harbor': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_column': "'Harbor'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'objectid': ('django.db.models.fields.IntegerField', [], {'db_column': "'OBJECTID'"})
        },
        'analysis.rockyshores': {
            'Meta': {'object_name': 'RockyShores'},
            'bc': ('django.db.models.fields.IntegerField', [], {}),
            'bm_cl': ('django.db.models.fields.IntegerField', [], {}),
            'com_u': ('django.db.models.fields.IntegerField', [], {}),
            'desig': ('django.db.models.fields.IntegerField', [], {}),
            'ed_u': ('django.db.models.fields.IntegerField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
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
            'size_field': ('django.db.models.fields.IntegerField', [], {}),
            'te_species': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'visitor': ('django.db.models.fields.IntegerField', [], {})
        },
        'analysis.shoreline': {
            'Meta': {'object_name': 'Shoreline'},
            'esi': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'esi_field': ('django.db.models.fields.FloatField', [], {}),
            'esi_id': ('django.db.models.fields.FloatField', [], {}),
            'esi_line_field': ('django.db.models.fields.FloatField', [], {}),
            'esi_line_i': ('django.db.models.fields.FloatField', [], {}),
            'fnode_1': ('django.db.models.fields.FloatField', [], {}),
            'fnode_field': ('django.db.models.fields.FloatField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'srid': '2992', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'line': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'lpoly_1': ('django.db.models.fields.FloatField', [], {}),
            'lpoly_field': ('django.db.models.fields.FloatField', [], {}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'rpoly_1': ('django.db.models.fields.FloatField', [], {}),
            'rpoly_field': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'source_id': ('django.db.models.fields.FloatField', [], {}),
            'tnode_1': ('django.db.models.fields.FloatField', [], {}),
            'tnode_field': ('django.db.models.fields.FloatField', [], {})
        }
    }
    
    complete_apps = ['analysis']
