from django.contrib.gis import admin
from omm.omm_manipulators.models import *


class EastOfTerritorialSeaLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date',)
    
admin.site.register(EastOfTerritorialSeaLine, EastOfTerritorialSeaLineAdmin)

class TerrestrialAndEstuariesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date',)
    
admin.site.register(TerrestrialAndEstuaries, TerrestrialAndEstuariesAdmin)

class TerrestrialAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date',)
    
admin.site.register(Terrestrial, TerrestrialAdmin)

class EstuariesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date',)
    
admin.site.register(Estuaries, EstuariesAdmin)