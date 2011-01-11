from django.contrib import admin
from omm.non_consumptive.models import NonConsumptive


class NonConsumptiveAdmin(admin.ModelAdmin):
    list_display = ('kml', 'active', 'creation_date',)
    
admin.site.register(NonConsumptive, NonConsumptiveAdmin)
