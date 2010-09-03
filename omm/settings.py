# Django settings for omm project.
from lingcod.common.default_settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#moved to settings_local
DATABASE_ENGINE = 'postgresql_psycopg2'
#DATABASE_NAME = 'oregon-marinemap'
#DATABASE_USER = 'postgres'

GEOMETRY_DB_SRID = 99999

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

#SECRET_KEY = 'keep_the_one_autogenerated_by_django-admin'

ROOT_URLCONF = 'omm.urls'

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

INSTALLED_APPS += ( 'tsp', 
                    'analysis',)

MPA_CLASS = 'tsp.models.AOI'
ARRAY_CLASS = 'tsp.models.AOIArray'
MPA_FORM = 'tsp.forms.AOIForm'
ARRAY_FORM = 'tsp.forms.ArrayForm'

COMPRESS_CSS['application']['source_filenames'] += (
    'omm/css/aoi_analysis.css',
)

# The following is used to assign a name to the default folder under My Shapes 
KML_UNATTACHED_NAME = 'Areas of Inquiry'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3j9~fjio+adjf93jda()#Jfk3ljf-ea9#$@#90dsfj9@0aj3()*fj3iow2f'

#These two variables are used to determine the extent of the zoomed in image in lingcod.staticmap
#If one or both are set to None or deleted entirely than zoom will default to a dynamic zoom generator
STATICMAP_WIDTH_BUFFER = .04
STATICMAP_HEIGHT_BUFFER = .12
#These two variables are used in conjunction with the above two variables to create a map extent indicator
#which is basically a rectangle on another map that outlines the extent of the zoomed in area (see oregon.xml)
STATICMAP_OUTLINE_X_OFFSET = .07
STATICMAP_OUTLINE_Y_OFFSET = .14

from settings_local import *
