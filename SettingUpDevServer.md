# Introduction #

**Please Note**:  Many of these steps are not appropriate for a production level server.
These are the steps that I took to get MarineMap Oregon up and running on the **dev server**.  Much of the following is based on the Oregon Marinemap Getting Started directions, which can be found from the documentation.marinemap.org site.


# Details #

MarineMap base app was already checked out into marinemap-src/marinemap

checkout oregon-marinemap into marinemap-src/oregon-marinemap
  * hg clone https://oregon-marinemap.googlecode.com/hg/ oregon-marinemap
  * had to remove the original oregon-marinemap folder since it wasn't empty

create omm/settings\_local.py
  * cp settings\_local.template settings\_local.py
  * uncomment and alter secret\_key
  * uncomment the 4 db lines
  * used marinemap as db rather than oregon
  * uncomment and change media\_root to /usr/local/marinemap-media/oregon-media
  * uncommented and changed the google api key
    * after registering for a new api key

finish lingcod install -- _not sure if this was necessary or not_
  * cd marinemap
  * python setup.py develop
  * python
  * from lingcod.common import default\_settings
  * print default\_settings.RELEASE
  * should all now work

setting up the database
  * sudo su gisdev
  * POSTGIS\_SQL\_PATH=`pg_config –sharedir`/contrib/postgis-1.5
    * postgis-1.5 was not mentioned in northcoast docs/getting\_started
    * might need to adjust the getting\_started docs?
  * createlang -d template1 plpgsql # Adding PLPGSQL language support.
  * psql -d template1 -f $POSTGIS\_SQL\_PATH/postgis.sql
    * Loading the PostGIS SQL routines
  * psql -d template1 -f $POSTGIS\_SQL\_PATH/spatial\_ref\_sys.sql
  * psql -d template1 -c "GRANT ALL ON geometry\_columns TO PUBLIC;"
    * Enabling users to alter spatial tables.
  * psql -d template1 -c "GRANT ALL ON spatial\_ref\_sys TO PUBLIC;"
  * psql -f /usr/local/marinemap-src/marinemap/lingcod/common/cleangeometry.sql -d template1 -U postgres
  * dropdb marinemap
  * createdb marinemap

add special projection to GeoDjango and to PostGIS
  * add the following definition (with srid 99999) to the bottom of share/proj/epsg (might need to run 'find /usr/local/share/ -name epsg' to find this file):
    * +proj=aea +ellps=GRS80 +lat\_0=41.0 +lon\_0=-117.0 +lat\_1=43.0 +lat\_2=48.0 +x\_0=700000.0 +y\_0=0 +datum=NAD83 +units=m +no\_defs
  * then run the following command from django shell in order to add the projection to the spatial\_ref\_sys table:
    * from django.contrib.gis.utils import add\_postgis\_srs
    * add\_postgis\_srs(99999)

some additional apache and wsgi work
  * created marinemap-src/oregon-marinemap/apache\_local
  * colin created/added apache\_local/oregon\_wsgi.py

colin pointed the chinook.marinemap.org apache config to the sites-enabled dir

stopped/started apache

added DEBUG = True to settings\_local.py (seems like this should be the case...for now)

install media
  * settings\_local.MEDIA\_ROOT = '/usr/local/marinemap-media/oregon-media/'
  * settings\_local.MEDIA\_URL = 'http://chinook.marinemap.org/media/' (_not sure if this was necessary nor not_)
  * mkdir oregon-marinemap/media (_if it doesn't exist already_)
  * python manage.py install\_media

DB continued...
  * python manage.py syncdb
  * python manage.py migrate

final touches
  * sudo touch ../apache\_local/oregon\_wsgi.py

add a study region
  * might start by using the sample study region (_this will be temporary_)
  * python manage.py dumpdata --format=json studyregion > tsp/fixtures/example\_data.json
  * python manage.py loaddata tsp/fixtures/example\_data.json
  * not sure if we should rather do the following:
    * python manage.py create\_study\_region --name oregon\_coast path\_to_/Study\_region
    * python manage.py change\_study\_region 1_

add a public layer
  * sudo chown -R root\: oregon-media/
  * sudo chmod -R 777 oregon-media/
  * both of the above were needed to get past permissions issues encountered when uploading public data layer
  * uploaded the water surface temperatures layer as an example (_also temporary_)

chinook.marinemap.org now shows study region, public layer, and allows drawing of mpas