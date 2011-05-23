from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.html import escape
from lingcod.features.models import PolygonFeature, FeatureCollection
from lingcod.features import register, alternate
from lingcod.layers.models import PrivateLayerList
from lingcod.manipulators.manipulators import ClipToStudyRegionManipulator
from lingcod.unit_converter.models import area_in_display_units

@register
class AOI(PolygonFeature):
    description = models.TextField(default="", null=True, blank=True)
    
    def convert_to_shp(self):
        '''
        Port the AOIs attributes over to the AOIShapefile model so we can export the shapefile.
        '''
        msf, created = AOIShapefile.objects.get_or_create(aoi=self)
        if created or msf.date_modified < self.date_modified:
            msf.name = self.name
            msf.aoi_id_num = self.pk
            msf.geometry = self.geometry_final
            #short_name = self.name
            if self.collection:
                msf.group = self.collection
                msf.group_name = self.collection.name
            #units based on the settings variable DISPLAY_AREA_UNITS (currently sq miles)
            msf.area_sq_mi = area_in_display_units(self.geometry_final)
            msf.author = self.user.username
            msf.aoi_modification_date = self.date_modified
            msf.save()
        return msf
    
    @property
    def kml(self):
        return """
        <Placemark id="%s">
            <visibility>1</visibility>
            <name>%s</name>
            <styleUrl>#%s-default</styleUrl>
            <ExtendedData>
                <Data name="name"><value>%s</value></Data>
                <Data name="user"><value>%s</value></Data>
                <Data name="desc"><value>%s</value></Data>
                <Data name="modified"><value>%s</value></Data>
            </ExtendedData>
            %s 
        </Placemark>
        """ % (self.uid, escape(self.name), self.model_uid(), 
               escape(self.name), self.user, escape(self.description), self.date_modified, 
               self.geom_kml)

    @property
    def kml_style(self):
        return """
        <Style id="%s-default">
            <BalloonStyle>
                <bgColor>ffeeeeee</bgColor>
                <text> <![CDATA[
                    <font color="#1A3752"><strong>$[name]</strong></font><br />
                    <p>$[desc]</p>
                    <font size=1>Created by $[user] on $[modified]</font>
                ]]> </text>
            </BalloonStyle>
            <PolyStyle>
                <color>778B1A55</color>
            </PolyStyle>
            <LineStyle>
                <color>ffffffff</color>
            </LineStyle>
        </Style>
        """ % (self.model_uid())

    @classmethod
    def mapnik_style(self):
        import mapnik
        polygon_style = mapnik.Style()
        ps = mapnik.PolygonSymbolizer(mapnik.Color('#DC640C'))
        ps.fill_opacity = 0.6
        ls = mapnik.LineSymbolizer(mapnik.Color('#ff0000'),0.2)
        ls.stroke_opacity = 1.0
        r = mapnik.Rule()
        r.symbols.append(ps)
        r.symbols.append(ls)
        polygon_style.rules.append(r)
        return polygon_style

    @property
    def hash(self):
        """"
        We only care about unique geometry+uid combinations;
        changing attributes don't really matter for the aes/nsh reports.
        """
        important = "%s%s" % (self.uid, self.geometry_final.wkt)
        return important.__hash__()

    class Options:
        manipulators = []
        optional_manipulators = [ 
                'omm_manipulators.manipulators.ExcludeTerrestrialManipulator', 
                'omm_manipulators.manipulators.ExcludeEstuariesManipulator', 
                'omm_manipulators.manipulators.ExcludeFederalWatersManipulator', 
                'omm_manipulators.manipulators.ExcludeStateWatersManipulator']
        geometry_input_methods = ['loadshp']
        verbose_name = 'Area of Interest (AOI)'
        show_template = 'mpa/show.html'
        form = 'tsp.forms.AOIForm'
        icon_url = 'common/images/mpa-.png'
        links = (
            alternate('Shapefile',
                'tsp.views.omm_shapefile',
                select='multiple single',
                type='application/zip',
            ),
        )


@register
class AOIArray(FeatureCollection):
        
    class Options:
        verbose_name = 'Folder'
        valid_children = ( 'tsp.models.AOI', 
                'tsp.models.AOIArray',
                'tsp.models.UserKml')
        form = 'tsp.forms.ArrayForm'
        show_template = 'array/show.html'
        links = (
            alternate('Shapefile',
                'tsp.views.omm_shapefile',
                select='multiple single',
                type='application/zip',
            ),
        )

    @classmethod
    def css(klass):
        return """ li.%(uid)s > .icon { 
        background: url('%(media)skmltree/dist/images/sprites/kml.png?1302821411') no-repeat -231px 0px ! important;
        } """ % { 'uid': klass.model_uid(), 'media': settings.MEDIA_URL }
    

class AOIShapefile(models.Model):
    """
    This model will provide the correct fields for the export of shapefiles using the django-shapes app.
    """
    geometry = models.PolygonField(srid=settings.GEOMETRY_DB_SRID,blank=True,null=True)
    name = models.CharField(max_length=255)
    aoi_id_num = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(AOIArray, null=True, blank=True)
    group_name = models.CharField(blank=True, max_length=255, null=True)
    area_sq_mi = models.FloatField(blank=True,null=True)
    author = models.CharField(blank=True, max_length=255,null=True)
    aoi = models.OneToOneField(AOI, related_name="aoi")
    aoi_modification_date = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    objects = models.GeoManager()

@register
class UserKml(PrivateLayerList):
    class Options:
        form = 'tsp.forms.UserKmlForm'
        show_template = 'userkml/show.html'
        export_png = False
        verbose_name = 'KML Upload' 
