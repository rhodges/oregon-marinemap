from lingcod.manipulators.manipulators import ClipToStudyRegionManipulator, manipulatorsDict

class ClipToTerritorialSeaManipulator(ClipToStudyRegionManipulator):

    class Options:
        name = 'ClipToTerritorialSea'
        display_name = "Clip to Territorial Sea"
        #description = "Clip your shape to the study region"
        html_templates = {
            '0':'omm_manipulators/territorialsea_clip.html', 
            '2':'omm_manipulators/outside_territorialsea.html', 
        }
        
manipulatorsDict[ClipToTerritorialSeaManipulator.Options.name] = ClipToTerritorialSeaManipulator