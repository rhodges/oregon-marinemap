# Summary #

Step by step account of my initial attempts at getting MarineMap Oregon setup and running on my machine.

# Introduction #

**PLEASE DO NOT USE this page as a reference for setting up MarineMap Oregon on your own machine (or any machine).**  For that purpose you'll want to use the MarineMap Oregon Getting Started page on the MarineMap documentation site.

The following is simply a documentation of the steps that I took to create the initial project, app, db, etc for MarineMap Oregon project on my local machine.

Most of the following steps were followed directly from the MarineMap creating\_new\_project docs @ http://maps11.msi.ucsb.edu/creating_new_project.html


# Details #

Using previously checked out version of Lingcod

Creating MPA/Array Classes
  * cd oregon-marinemap
  * django-admin.py startproject mmo

Settings modifications
  * used settings from creating\_new\_project docs
  * used settings\_local from nc\_mlpa as a template,
  * changed db info, secret\_key, and media\_root (in settings\_local)
  * removed db info from settings (assigned in settings\_local)
  * added "from settings\_local import " to bottom of settings.py
  * ...at some point I also added ROOT\_URLCONF = 'omm.urls' to settings...

Creating MPA/Array classes
  * cd mmo
  * python manage.py startapp tsp
  * copied models and forms from creating\_new\_project docs

URLS
  * copied urls.py from creating\_new\_project docs into mmo/urls.py
  * added import settings to top of mmo/urls.py

DB
  * added cleangeometry to template-postgis
  * (copy contents of marinemap/lingcod/common/cleangeometry.sql into psql terminal command prompt (or psql -f <path to cleangeometry.sql> -d template1 -U postgres))
  * created omm db with template-postgis (used pgadmin)

Study Region
  * geometry\_db\_srid = 2992 (not 32610)
  * matched srid to study region (2992)
  * http://spatialreference.org/ref/epsg/2992/
  * searched for Oregon
  * matched proj4 data http://spatialreference.org/ref/epsg/2992/proj4/ with qgis properties
  * dropped db (after dropping mm\_study\_region, syncdb and migrate failed to regenerate it)
  * syncdb, migrate
  * migrate did bark once on lingcod/spacing/fixtures/south\_initial\_data.json
    * IntegrityError:  new row for relation “spacing\_spacingpoint” violates check constraint “enforce\_srid\_geometry”
  * python manage.py create\_study\_region --name oregon\_coast <path to sr>/Study\_region
  * python manage.py change\_study\_region 1

Migrating MLPA
  * python manage.py schemamigration --initial tsp
  * python manage.py migrate tsp --fake

Media
  * create dev\oregon-marinemap\media directory
  * media\_root = 'U:/dev/oregon-marinemap-media/media/'
  * python manage.py install\_media

Deployment
  * python manage.py site\_setup\_for\_dev
  * python manage.py sharing\_setup
  * python manage.py runserver
  * localhost:8000 works, displays oregon sr

drawing shape now clips and saves

added public layers via admin, from lingcod.layers.fixtures.public\_layers.html
as explained here: http://maps11.msi.ucsb.edu/layers.html