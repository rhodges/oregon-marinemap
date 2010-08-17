from django.contrib.contenttypes.models import ContentType
from lingcod.unit_converter.models import length_in_display_units
    
default_value = '---'

'''
General method for obtaining the nearest geometries from a given model
Returns a list of tuples [(name, distance)] 
Requires the given model to have a field called 'name'
'''    
def get_nearest_geometries(nsh, model_name, length=3):    
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    tuples = [(shape.geometry.centroid.distance(nsh.geometry_final), shape) for shape in shapes]
    tuples.sort()
    tuples = tuples[:length]
    nearest_shapes = []
    for tuple in tuples:
        nearest_shapes.append(tuple[1].name)
    return nearest_shapes
    
'''
General method for obtaining the nearest geometries from a given model along with their distances
Returns a list of tuples [(name, distance)] 
Requires the given model to have a field called 'name'
'''    
def get_nearest_geometries_with_distances(nsh, model_name, length=3):    
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    tuples = [(shape.geometry.centroid.distance(nsh.geometry_final), shape) for shape in shapes]
    tuples.sort()
    tuples = tuples[:length]
    nearest_shapes = []
    for tuple in tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_shapes.append( (name, distance) )
    return nearest_shapes
    
'''
General method for obtaining the intersecting geometries from a given model 
Returns a list of shape names or a list containing a single default value ('---') if no intersecting shapes were found
Requires the given model to have a field called 'name'
'''    
def get_intersecting_geometries(nsh, model_name):
    model_class = ContentType.objects.get(model=model_name).model_class()
    shapes = model_class.objects.all()
    intersecting_shapes = [shape.name for shape in shapes if shape.geometry.intersects(nsh.geometry_final)]
    if len(intersecting_shapes) == 0:
        intersecting_shapes.append(default_value)
    return intersecting_shapes    
    
    