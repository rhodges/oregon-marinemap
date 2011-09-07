from django.contrib.gis.db import models
#Used for Caching Report Context
from picklefield import PickledObjectField
    
class EconCache(models.Model):
    aoi_id = models.IntegerField()
    type = models.CharField(max_length=50)
    context = PickledObjectField()
    wkt_hash = models.CharField(max_length=255)
    
    #ensure no duplicates (same geometry and type) 
    def save(self, *args, **kwargs):
        #remove any old entries
        old_entries = EconCache.objects.filter(wkt_hash=self.wkt_hash, type=self.type)
        for entry in old_entries:
            EconCache.delete(entry)
        #save the new entry
        super(EconCache, self).save(*args, **kwargs)
        
    class Meta:
        app_label = 'analysis'
