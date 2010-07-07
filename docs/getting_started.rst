.. _getting_started:

Getting Started
===============


Introduction
************

These instructions will walk you through developing a basic implementation of
MarineMap Oregon. This includes installing the Lingcod base app and the Oregon specific app 
from the development repository, setting up a database, testing that everything installed smoothly, then doing some
basic customization. By the end you'll have an application that will perform
all the `basic functions <http://code.google.com/p/marinemap/wiki/FeaturesAndRequirements>`_
needed to start drawing MPAs on a map.


Project Structure
*****************

It is important to understand how a MarineMap application is structured. There are essentially two codebases:

    * Lingcod - a python module providing a set of django apps that contain the core functionality common to all MarineMap instances.
    * the project code - in this case, MarineMap Oregon, a django project that implements and extends the functionality provided by Lingcod.

By seperating the two codebases, we can more easily maintain multiple MarineMap projects while continuing to improve the underlying core functionality.


Install Dependencies
********************

There are various dependencies required for both the base project and the Oregon specific project.  
Before you proceed any further on the MarineMap Oregon specific site, you will need to install 
Lingcod's dependencies and Lingcod itself. For detailed instructions, please follow
the `Getting Started <http://maps11.msi.ucsb.edu/getting_started.html>`_ documentation for the Lingcod base application.
 
 
Installing MarineMap Oregon
***************************

After you have worked through the `Getting Started <http://maps11.msi.ucsb.edu/getting_started.html>`_ documentation for the Lingcod base application, 
you are now ready to install the MarineMap Oregon specific project.  

First you will need to checkout a copy of the default branch of MarineMap Oregon from the `project page <http://code.google.com/p/oregon-marinemap/source/checkout>`_ ::

     cd ~/src
     hg clone https://oregon-marinemap.googlecode.com/hg/ oregon-marinemap

     
Using settings.py and settings_local.py
---------------------------------------

Take a look at ``oregon-marinemap/omm/settings_local.template`` and 
``settings.py``. MarineMap uses a simple splitsetting scheme as described 
`here <http://code.djangoproject.com/wiki/SplitSettings#Multiplesettingfilesimportingfromeachother>`_. 
What this enables is the ability to specify standard 
settings in settings.py and commit them to a public repository, but these
don't correspond to any particular machine. You then create a 
``settings_local.py`` file on the machine for deployment or development from the
template, and it contains your passwords and such.

Lets do that now. Copy ``settings_local.template`` to ``settings_local.py``, then
uncomment the following line::

    # SECRET_KEY = '3j9~fjio+adjf93jda()#Jfk3ljf-ea9#$@#90dsfj9@0aj3()*fj3iow2f'

Alter ``SECRET_Key`` to make it unique. Next uncomment and alter the following
lines as needed to allow this application to connect to your local database::

    # DATABASE_NAME = 'oregon'
    # DATABASE_USER = 'postgres'
    # DATABASE_PASSWORD = 'my-secret-password'
    
    
Handling Media
--------------
Because a MarineMap instance is split between Lingcod (core functionality) and the project-specific code, 
static media files such as html, javascript, css, images, etc. may exist in both. Django, however, expects 
all the static media to be in a single directory. In order to merge the Lingcod media with the project media, 
you need to create a third (empty) media directory and set it as your ``MEDIA_ROOT`` in the project 
``settings_local.py`` ::

    mkdir /src/oregon-marinemap-media/
    cd ~/src/oregon-marinemap/omm/
    echo "MEDIA_ROOT='/src/oregon-marinemap-media'" >> settings_local.py

Then use the 'install_media' management command to merge all the media files into the ``MEDIA_ROOT`` directory::

    python manage.py install_media


setup the database
------------------

Create a database, accessible by the connection settings above, using a tool
like `pgAdmin <http://www.pgadmin.org/>`_. It is very important that this
database be created from a template with all the PostGIS functions installed. One approach
is to set up postgis in the default postgres database called template1::

   #run as postgres superuser
   POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib
   createlang -d template1 plpgsql # Adding PLPGSQL language support.
   psql -d template1 -f $POSTGIS_SQL_PATH/postgis.sql # Loading the PostGIS SQL routines
   psql -d template1 -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
   psql -d template1 -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
   psql -d template1 -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

Once the template is spatially enabled, create your project database::

   createdb oregon -U postgres

To setup the database schema and populate with some initial data, run the 
django syncdb command from within the ``oregon-marinemap/omm`` directory::

    python manage.py syncdb

And then use the migrate command which will handle creating the schemas and populating the database
for those applications which are under `migration control <http://south.aeracode.org/docs/about.html>`_::

    python manage.py migrate
    
.. note::
    
    If syncdb fails and you get an error related to importing settings.py 
    failing, you are likely missing a python dependency. Double-check 
    `the dependencies <http://maps11.msi.ucsb.edu/getting_started.html#dependencies>`_, 
    and if none are missing jump into a python shell from
    ``oregon-marinemap/omm``, ``import settings``, and look for any errors.

    
Verify and Run the dev server
-----------------------------

Confirm that everything is working as expected by running the tests::
    
    python manage.py test
    
If everything looks good, turn on the dev server::
    
    python manage.py runserver
    
Hit http://localhost:8000/admin/ in a browser and use the authentication
credentials specified when syncdb was run.

At http://localhost:8000/ the interface should render with sample data.


Next Steps
**********
Now that you have installed the Oregon MarineMap software, you can begin to use/customize it. Please refer to:
    * The core `Lingcod documentation <http://maps11.msi.ucsb.edu/index.html>`_.

