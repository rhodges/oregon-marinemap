# Potential Manipulative Strategies #

Clip AOI to a study region (such as the Territorial Sea) when the shape is drawn
  * This is the simplest strategy in that this process is built in to MarineMap already, and the analysis and reporting (provided the layers used for analysis are clipped the study region as well) can be assumed to be accurate.
  * MarineMap is also set up to clip against multiple shapes at draw time and provided these shapes are to be used every time a shape is drawn (and in the same order), this can be implemented easily.
  * It should also be noted that the 'study region' could be as broad as the state boundaries of Oregon that include the Territorial Sea, or it could simply be the Territorial Sea itself with (or without) estuaries.

Keep the AOI as-is (without any clipping)
  * While it is easy to have the application accept the AOI as it's drawn -- without any clipping -- this possibility has the potential to increase complexity in other areas.
  * Deciding, for the purposes of analysis for example, whether an AOI falls within the analysis datasets (and how much it falls within those boundaries -- do we care if only 1% of the AOI falls outside the boundary?  or maybe the user intended the AOI to be within the boundaries but failed to draw it accurately...) introduces both complexity in development and ambiguity in the results.  The former may require time we don't have and the latter may introduce problems we don't want.
