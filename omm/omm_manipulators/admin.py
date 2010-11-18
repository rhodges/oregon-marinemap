from django.contrib.gis import admin
from omm.omm_manipulators.models import EastOfTerritorialSeaLine


class EastOfTerritorialSeaLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date',)
    
admin.site.register(EastOfTerritorialSeaLine, EastOfTerritorialSeaLineAdmin)
