# Raster Processing #

In the following example, I'll use a geotiff called grb\_all\_skd.
Note:  This can also be done on a local machine given appropriate settings and software.

  * Copy geotiff to dev server `EBS_fishingmaps/display/temp/`

  * Process the data (generate the kml/superoverlay) from within `temp/grb_maps/`
    * `python ../../scripts/pre-render-raster.py -i grb_all_skd.tif -g ../../scripts/gdal2tiles.py -s 0 -e 9`
  * the kml/superoverlay is now in `EBS_fishingmaps/display/temp/grb_maps/grb_all_skd/`

  * Copy the data to `EBS_fishingmaps/display/public_maps/`
    * `mv grb_all_skd EBS_fishingmaps/display/public_maps/grb_agg`
    * Note:  Naming convention for omm uses _port-abbreviation\_group-abbreviation_
      * groups are Commercial (com), Charter Boat (char), Recreational Sport Boat (rec), and Cross-Sector (agg)

  * Remove the `grb_maps` folder from `display/temp/`

  * Copy the data back to local machine for viewing and testing kml changes


# Vector Processing #

In the following example, I'll use a shapefile called grb\_all\_kd\_line.
Note:  This can also be done on a local machine given appropriate settings and software.

  * Copy shapefile to dev server `EBS_fishingmaps/display/temp`/

  * Process the data (generate the kml/superoverlay) from within `EBS_fishingmaps/display/scripts`
    * `python pre-render-vector.py -v ../temp/grb_contours/grb_all_kd_line.shp -w temp/grb_pvc -s 0 -e `5
  * the kml/superoverlay is now in `EBS_fishingmaps/display/scripts/temp/grb_pvc/grb_contours/grb_all_kd_line/`

  * Copy the data to `EBS_fishingmaps/display/public_contours/`
    * mv temp/grb\_pvc/grb\_contours/grb\_all\_kd\_line ../public\_contours/grb\_agg`
    * Note:  Naming convention for omm uses _port-abbreviation\_group-abbreviation_
      * groups are Commercial (com), Charter Boat (char), Recreational Sport Boat (rec), and Cross-Sector (agg)

  * Remove the `grb_contours` folder from `scripts/temp/`

  * Copy the data back to local machine for viewing and testing kml changes

# Modifying the Fishing Data Layers KML #

  * Note:  the most recent kml can always be downloaded from the admin
    * Fishing\_layers > Public fishing layers
  * Note:  kml is ordered north to south
  * After kml has been modified to reference the new fishing data layer, upload this kml via the admin on the local machine and the dev server and test for suitable LookAt (lat/long and range), suitable description, and working maps and contours.