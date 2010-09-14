from django.contrib import admin

from django.contrib.auth.models import Permission
admin.site.register(Permission)

from omm.tsp.models import AOI

class AOIAdmin(admin.ModelAdmin):
    list_display = ( 'pk', 'name', 'user', 'date_created', 'date_modified')
    search_fields = ('name','id','user__username','user__first_name','user__last_name')
    
admin.site.register(AOI, AOIAdmin)