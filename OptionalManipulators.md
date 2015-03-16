Given checkboxes for the following:
  * Clip to Territorial Sea line
  * Clip to Shoreline
  * Include Estuaries

How can we can satisfy the following clipping requests from users?
  * Shape should be left as it is
    * no clipping selection made (all checkboxes left un-selected)
  * Shape should not extend beyond the territorial sea line
    * Clip to Territorial Sea line
  * Shape should not include any state waters (deep-sea only)
    * Clip to Territorial Sea line
  * Shape should be contained within the territorial sea line and the shoreline, excluding estuaries
    * Clip to Territorial Sea line, Clip to Shoreline
  * Shape should be contained within the territorial sea line and the shoreline, including estuaries
    * Clip to Territorial Sea line, Clip to Shoreline, Include Estuaries
  * Marine-based shape that includes entire shape from shoreline, including estuaries
    * Clip to Shoreline, Include Estuaries
  * Land-based shape that includes entire shape from shoreline, including estuaries
    * Clip to the Shoreline, Include Estuaries
  * Marine-based shape that includes entire shape from shoreline, excluding estuaries
    * Clip to the Shoreline
  * Land-based shape that includes entire shape from shoreline, excluding estuaries
    * Clip to the Shoreline
  * Estuaries only
    * Include Estuaries

Note, for requests that have the same solution, such as the following:
  * Marine-based shape that includes entire shape from shoreline, excluding estuaries
    * Clip to Shoreline
  * Land-based shape that includes entire shape from shoreline, excluding estuaries
    * Clip to Shoreline
A single selection (de-selection) of the Clip to Shoreline could suffice, as the tool could simply offer the largest of the two polygons created when clipping against the shoreline.  Imagine a shape that is almost entirely marine-based but overlaps the shoreline a little (90% marine, 10% land).  It's most likely the user is intending the shape to be marine-based and not land-based.  And so when the tool clips against the shoreline, it will 'guess' the user's intention based on the marine-based result being larger than the land-based result.  And of course, if the tool ever guesses incorrectly, the user will always be given the chance to edit their shape before submitting it.

A problem arises when the user selects the only combination we don't address above:

  * Clip to Territorial Sea line **and** Include Estuaries

One way to deal with this problem might be by allowing both of the following:
  * Clip to Territorial Sea line, Include Estuaries, AND
  * Clip to Territorial Sea line
to do the same thing...

#  #

### Internal Layers ###

Given either of the above solutions, what geometries might be needed for the actual clipping?
  * layer that includes everything 'east' of the territorial sea line
  * _layer that includes everything 'west' of territorial sea line_
  * layer that includes everything 'east' of a shoreline that includes estuaries
  * layer that includes everything 'east' of a shoreline that excludes estuaries
  * _layer that includes everything 'west' of a shoreline that includes estuaries_
  * _layer that includes everything 'west' of a shoreline that excludes estuaries_
  * layer that includes estuaries only