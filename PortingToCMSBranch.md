# Introduction #

Marinemap had previously been hardcoded to deal with the concepts of MPAs and Arrays (terminology from the MLPA process). While those ideas could be extended to work in other contexts (as it was with oregon), it is somewhat limiting.

The CMS or marinemap 3.0 branch was developed to provide a framework for Features and Feature Collections which would be more extensible than the previous codebase.

Here are the main tasks required to port the oregon-marinemap application over to marinemap 3.0:

## Current Status (Fri 4/1/2011) ##
  * Forms and templates for AOIs have been ported.
  * AOIs and AOI groups have been fully ported to the Features API.
  * Migrations written to smoothly move data b/t versions.
  * Permissions for analysis reports now uses Features sharing API.
  * Staticmap was refactored to use feature uids, generate overview maps and temp maps on disk. Maps work in all html and pdf reports.
  * Inherit urls from lingcod
  * Moved several useful utility functions into lingcod core
  * Removed internal references to old mpa, array, sharing and rest apps.
  * Added some Options to manipulators to make them Feature API compliant.
  * Support for privatedatalayers - user uploaded kml files - as features.
  * Support for privatesuperoverlays - tiled data available to select groups - and implemented a seperate sharing scheme for these since they are not Features.

Main TODOs at this point are kmlEditor UI behavior, fixing any bugs that that brings to light, docs, unit tests (at this point nothing OMM-specific is really unit tested) and lots of real live testing.

## details ##

Subclass PolygonFeature and FeatureCollection (instead of MPA and Array) and tweak model Options to match features API

Designation model for AOIs

Subclass lingcod.feature.FeatureForm for forms.

Remove all references to lingcod.mpa, lingcod.array, lingcod.rest, lincod.sharing and replace with apropos CMS functions (all within lingcod.features now)

Staticmap API has changed and requires additional dependencies.

KML templates will need to be adjusted for new context variables.

Remove private kml layers from Data Layers tab (will be treated as features)

Optional manipulators specified by class name string.

Manipulators must specify their supported geometry types.

Migrations to port the data models to new structure

## questions ##

Should we treat the nsh and aes geographic models as Features?

Do we need data migrations to convert data from previous version?

Need to limit creation of user kml layers to certain groups? Will require core lingcod changes (about 1 day)