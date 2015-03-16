#Summary Discussion on integration of OWET Cum. Effects Tool data products into OMM

Meeting on Nov. 12, 2010 @ Ecotrust.  Tim Welch, Tanya Haddad, Kevin Halsey, Paul Manson

# Introduction #
Parametrix is finishing up a multicriteria analysis tool for OWET that quantifies suitability of a given area for renewable energy projects using a wide variety of criteria.
  * Current phase of the project wraps up in June 2011

# Analysis #
  * The geographic extent of the analysis is the oregon coast west into the ocean and East to roughly the Cascades.
  * The analysis produces a cost surface (raster) for each criteria.
  * There will be up to 240 criteria, up to 40 for each of 6 questions as far as I know.
  * The cells for this surface match up with the planning unit grid developed by DLCD.
  * The resulting cost surfaces can be exported from the tool, with symbology, as a GeoTiff and it's expected that these are what can be used within MarineMap.
  * Cell values range from roughly 0 to 1000.  These values are unit-less.

# Integration #
At this time we are not considering integrating the cumulative effects tool into MarineMap such that users can use this tool through the Marinemap interface.  We are considering a much looser level of integration where MarineMap data products from the tool will be made available in Oregon MarineMap.

We think there are two ways that data products from the OWET tool can be used in OMM: visualization and further analysis

## Visualization ##
Like the consumptive and non-consumptive maps that Ecotrust has developed, the cost surface layers from this tool can be be converted to KML superoverlays and visualized on top of the Google Earth map.

  * V1. The simplest implementation would be for DLCD and other partners to develop a canned set of 'scenarios' using the OWET tool, where a 'scenario' is one complete set of cost surface rasters for all of the criteria for a specific purpose.  Assuming I, Tim, understand things correctly there may be a desire for multiple scenarios to be developed.  Each 'scenario' would have up to 240 cost surfaces in the complete set which is quite a few.  A complete set of rasters for a scenario would be imported into MarineMap and made available for viewing.  This could be done much like the non-consumptive recreation layers in OMM which allow users to load up an individual layer and click a specific cell grid viewing the cost value associated with it.  These complete scenarios could be developed in the OWET cum. effects tool by stakeholder groups and then submitted for inclusion into MarineMap.  This would force stakeholders groups to come to agreement and reduce the number of scenarios coming into Oregon MarineMap.

  * V2. The next step in visualization is much more complicated to give fair warning.  It involves allowing users to take their own geotiff's they've exported from the OWET Cum. Effects tool and import them into MarineMap as their own custom data layer for viewing.  A complete set of cost surface rasters for all criteria would be very big so I could imagine us allowing the user to upload individual maps for a given criteria and not all at once.  The benefit to this import features is that the user is not limited to just the canned scenarios in OMM.  This feature is only useful to power users, of which there are not expected to be a significant number, and would not likely be used by general users.  The fact that the user can change the symbolology (coloring) of the output in the OWET tool makes consistency and usability an issue.  There is also the fact that information on how to interpret these layers would need to be provided in order for other users to be able to make use of this product.  So the solution is not clear and for this reason, V2 is recommended as a second step implemented only when the need is clearly shown.  Further, if implemented we should consider making these user-uploaded layers only accessible by the person that uploaded them to reduce some of the complexity and usability issues.

## Cum. Effects Reports in OMM ##
Moving beyond visualization it would be possible to take the cost surface rasters from the cum. effects tool that have been brought into MarineMap and run further analysis against an area of inquiry (AOI) drawn in OMM by a user.

  * [R1](https://code.google.com/p/oregon-marinemap/source/detail?r=1). The simplest implementation would be to use the canned scenarios and allow the user to summarize the cost within a given AOI for a set of criteria.  This summarization of the costs could be presented in a number of ways yet to be determined.  It would be useful to look at how the RadMap viewer presents information.  The user could pre-select which criteria they are interested in from the 240 or so.  Saving their selections from the past run would be appropriate.

  * [R2](https://code.google.com/p/oregon-marinemap/source/detail?r=2). The next step in reporting is again much more complicated, building on [R2](https://code.google.com/p/oregon-marinemap/source/detail?r=2) and involves allowing the user to produce these reports for scenarios that they've uploaded from their own runs of the OWET cum. effects tool.  this builds on the user import feature described in the viz section above.  This would provide the most flexibility but also the most complexity.

## Recommendation ##
Recommended by dev group that we proceed with V1 with a go ahead from DLCD/OWET and implement [R1](https://code.google.com/p/oregon-marinemap/source/detail?r=1) only if useful analysis is defined and requests by enough people.  V2 and [R2](https://code.google.com/p/oregon-marinemap/source/detail?r=2) are quite complex and we recommending not moving forward with these without need being shown through use of V1 and [R1](https://code.google.com/p/oregon-marinemap/source/detail?r=1).

## Developer Time Estimates ##
V1. 1-2 weeks to load and review one or more complete scenarios worth of cost surface rasters in Oregon MarineMap.

V2. 4-6 weeks to design, implement and test the ability for users to upload and view cost surface layers they've developed in the OWET cumulative effects tool.  One issue here is that users can create their own symbology.  We may have to override this in the tool for consistency.

[R1](https://code.google.com/p/oregon-marinemap/source/detail?r=1). 2-3 weeks to define, implement and review summarized reports for AOI's against one or more criteria for the canned scenarios.

[R2](https://code.google.com/p/oregon-marinemap/source/detail?r=2).  2-4 weeks.  Details not fully clear at this point.  Builds upon the previous three options.

# Timeline #
It's not expected that the Oregon MarineMap team will be able to address the integration of products from the OWET cumulative effects tool until after the end of 2010.  We will reconvene in January to plan out the way forward more fully.  The OWET tool should support our needs as-is so further development work is not anticipated to be needed on the part of Parametrix.

# Parametrix Future Work #
  * Related to the OWET Cumulative Effects project work is the the assessment of confidence values along with costs using Bayesian analysis.  This would provide bounds on uncertainty for a given criteria and point out areas of concern.
  * This piece of work adds more dimensions to the resulting data products including temporal making it more difficult to visualize.  There may be potential to use these more complex data products for analysis within Oregon MarineMap but not necessarily visualization as we are limited to 2-3 dimensions.