from django.core.management import setup_environ
import os
import sys
sys.path.append(os.path.dirname(__file__))

import settings
setup_environ(settings)

#==================================#
from tsp.models import AOI, AOIArray, UserKml
from django.contrib.gis.geos import GEOSGeometry 
from django.contrib.auth.models import User, Group
from lingcod.common.utils import enable_sharing
from django.core.files import File

def main():
    user = User.objects.get(username='perry')

    for model in [AOI, AOIArray, UserKml]:
        a = model.objects.all()
        for i in a:
            i.delete()
    
    g1 = GEOSGeometry('SRID=4326;POLYGON((-124.089 45.215, -124.011 45.215, -124.011 45.284, -124.089 45.284,-124.089 45.215))')
    g1.transform(settings.GEOMETRY_DB_SRID)
    aoi1 = AOI(user=user, name="AOI1", geometry_orig=g1) 
    # geometry_final will be set with manipulator
    aoi1.save()

    g2 = GEOSGeometry('SRID=4326;POLYGON((-124.112 45.084, -124.030 45.084, -124.030 45.171, -124.112 45.171,-124.112 45.084))')
    g2.transform(settings.GEOMETRY_DB_SRID)
    aoi2 = AOI(user=user, name="AOI2", geometry_orig=g2) 
    # geometry_final will be set with manipulator
    aoi2.save()

    g2 = GEOSGeometry('SRID=4326;POLYGON((-124.112 45.084, -124.030 45.084, -124.030 45.171, -124.112 45.171,-124.112 45.084))')
    g2.transform(settings.GEOMETRY_DB_SRID)
    aoi3 = AOI(user=user, name="AOI3 Not Shared", geometry_orig=g2) 
    # geometry_final will be set with manipulator
    aoi3.save()
    print "######", aoi3.uid

    array1 = AOIArray(user=user, name="AOI Group 1")
    array1.save()

    array2 = AOIArray(user=user, name="AOI SubGroup 1.1")
    array2.save()

    aoi1.add_to_collection(array1)
    aoi2.add_to_collection(array2)
    array2.add_to_collection(array1)

    ####
    try:
        user2 = User.objects.get(username="user2")
    except:
        user2 = User.objects.create_user('user2', 'test@marinemap.org', password='pass')

    try:
        group1 = Group.objects.get(name="Group1")
    except:
        group1 = Group.objects.create(name="Group1")

    group1.save()
    user.groups.add(group1)
    user2.groups.add(group1)
    enable_sharing(group1)

    group2 = Group.objects.get(name=settings.SHARING_TO_PUBLIC_GROUPS[0])
    user.groups.add(group2)
    enable_sharing(group2)
    array1.share_with(group2)

    userkml = UserKml(user=user, name="Moab KML track")
    userkml.save()
    path = os.path.dirname(os.path.abspath(__file__))
    f = File(open(path + '/fixtures/test_moab.kml'))
    userkml.kml_file.save('test.kml', f)
    userkml.add_to_collection(array1)


if __name__ == '__main__':
    main()
