from django.contrib.contenttypes.models import ContentType
from lingcod.unit_converter.models import length_in_display_units
    
'''
'''    
default_value = '---'

'''
ensures the given type is either of the form that is to be used in the db, or is None
'''
def ensure_type(type):
    if type_is_geo(type):
        return 'Geography'
    if type_is_phy(type):
        return 'Physical'
    if type_is_bio(type):
        return 'Biology'
    if type_is_hum(type):
        return 'Human'
    else:
        return None
    
def type_is_geo(type):
    lc_type = type.lower()
    if lc_type in ['geo', 'geography']:
        return True
    return False
    
def type_is_phy(type):
    lc_type = type.lower()
    if lc_type in ['phy', 'physical']:
        return True
    return False
    
def type_is_bio(type):
    lc_type = type.lower()
    if lc_type in ['bio', 'biology']:
        return True
    return False
    
def type_is_hum(type):
    lc_type = type.lower()
    if lc_type in ['hum', 'human']:
        return True
    return False

'''
General method for obtaining the nearest geometries from a given model
Returns a list of nearest objects
'''    
def get_nearest_geometries(aoi, model_name, length=3):    
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    tuples = [(shape.geometry.centroid.distance(aoi.geometry_final), shape) for shape in shapes]
    tuples.sort()
    tuples = tuples[:length]
    nearest_shapes = []
    for tuple in tuples:
        nearest_shapes.append( tuple[1] )
    return nearest_shapes
    
'''
General method for obtaining the nearest geometries from a given model along with their distances
Returns a list of tuples [(name, distance)] 
Requires the given model to have a field called 'name'
'''    
def get_nearest_geometries_with_distances(aoi, model_name, line=False, length=3):    
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    if not line:
        tuples = [(shape.geometry.centroid.distance(aoi.geometry_final), shape) for shape in shapes]
    else:
        tuples = [(shape.geometry.distance(aoi.geometry_final), shape) for shape in shapes]
    tuples.sort()
    tuples = tuples[:length]
    nearest_shapes = []
    for tuple in tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(aoi.geometry_final))
        nearest_shapes.append( (name, distance) )
    nearest_shapes = sorted(nearest_shapes, key=lambda shapes: shapes[1])
    return nearest_shapes
    
'''
General method for obtaining the intersecting geometries from a given model 
Returns a list of shape names or a list containing a single default value ('---') if no intersecting shapes were found
Requires the given model to have a field called 'name'
'''    
def get_intersecting_geometries(aoi, model_name):
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    intersecting_shapes = [shape.name for shape in shapes if shape.geometry.intersects(aoi.geometry_final)]
    return intersecting_shapes    
    
    