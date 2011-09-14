from django.contrib import admin
from omm.fishing_layers.models import PublicFishingLayer


class PublicFishingLayerAdmin(admin.ModelAdmin):
    list_display = ('kml', 'active', 'creation_date',)
    
admin.site.register(PublicFishingLayer, PublicFishingLayerAdmin)
