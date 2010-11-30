from django.contrib import admin
from analysis.models import *

class NSHCacheAdmin (admin.ModelAdmin):
    list_display = ()

admin.site.register(NSHCache, NSHCacheAdmin)

class AESCacheAdmin (admin.ModelAdmin):
    list_display = ()

admin.site.register(AESCache, AESCacheAdmin)