from lingcod.manipulators.manipulators import BaseManipulator, ClipToStudyRegionManipulator, ClipToShapeManipulator, manipulatorsDict
from omm.omm_manipulators.models import EastOfTerritorialSeaLine
#the following might be temporary for limited use in MyClipToShapeManipulator
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from lingcod.common.utils import LargestPolyFromMulti


#using the following to override incomplete ClipToShapeManipulator.manipulate method in lingcod
#we can remove this class, method and reference thereof when Lingcod is next updated
class MyClipToShapeManipulator(ClipToShapeManipulator):

    def manipulate(self):
        #extract target_shape geometry
        target_shape = self.target_to_valid_geom(self.target_shape)
        
        #extract clip_against geometry
        try:
            clip_against = GEOSGeometry(self.clip_against)
            clip_against.set_srid(settings.GEOMETRY_CLIENT_SRID)
        except Exception, e:
            raise self.InternalException("Exception raised in ClipToShapeManipulator while initializing geometry on self.clip_against: " + e.message)
        
        if not clip_against.valid:
            raise self.InternalException("ClipToShapeManipulator: 'clip_against' is not a valid geometry")
        
        #intersect the two geometries
        try:
            clipped_shape = target_shape.intersection( clip_against )
        except Exception, e:
            raise self.InternalException("Exception raised in ClipToShapeManipulator while intersecting geometries: " + e.message)  
        
        #if there was no overlap (intersection was empty)
        if clipped_shape.area == 0:
            status_html = self.do_template("2")
            message = "intersection resulted in empty geometry"  #ALTERATION #1
            #return self.result(clipped_shape, target_shape, status_html, message)
            raise self.HaltManipulations(message, status_html)   #ALTERATION #2
         
        #if there was overlap
        largest_poly = LargestPolyFromMulti(clipped_shape)
        status_html = self.do_template("0")
        #message = "'target_shape' was clipped successfully to 'clip_against'"
        #return self.result(largest_poly, target_shape, status_html, message)
        return self.result(largest_poly, status_html)

class ExcludeFederalWatersManipulator(MyClipToShapeManipulator):

    def __init__(self, target_shape, **kwargs):
        self.target_shape = target_shape
        try:
            self.clip_against = EastOfTerritorialSeaLine.objects.current().geometry
            self.clip_against.transform(settings.GEOMETRY_CLIENT_SRID)
        except Exception, e:
            raise self.InternalException("Exception raised in ExcludeFederalWatersManipulator while obtaining exclude-from-federal-waters-manipulator geometry from database: " + e.message)    

    class Options:    
        name = 'ExcludeFederalWatersManipulator'
        display_name = 'Exclude Federal Waters'
        description = 'Removes any part of user drawn shape that is beyond the territorial sea line.'

        html_templates = {
            '0':'omm_manipulators/exclude_federal_waters.html',
            '2':'omm_manipulators/empty_result.html',
        }

manipulatorsDict[ExcludeFederalWatersManipulator.Options.name] = ExcludeFederalWatersManipulator
        
class ClipToTerritorialSeaManipulator(ClipToStudyRegionManipulator):

    class Options:
        name = 'ClipToTerritorialSea'
        display_name = "Clip to Territorial Sea"
        #description = "Clip your shape to the study region"
        html_templates = {
            '0':'omm_manipulators/territorialsea_clip.html', 
            '2':'omm_manipulators/outside_territorialsea.html', 
        }
        
manipulatorsDict[ClipToTerritorialSeaManipulator.Options.name] = ClipToTerritorialSeaManipulator

