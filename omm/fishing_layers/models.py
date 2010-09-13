from django.db import models

class PublicFishingLayer(models.Model):
    """Model used for storing uploaded kml files that list all public fishing data layers.

        ======================  ==============================================
        Attribute               Description
        ======================  ==============================================
        ``creation_date``       When the layer was created. Is not changed on
                                updates.
                                
        ``active``              Whether this kml file represents the currently 
                                displayed data layers. If set to true and 
                                another ``EcotrustLayerList`` is active, that 
                                old list will be deactivated.

        ``kml``                 Django `FileField <http://docs.djangoproject.com/en/dev/ref/models/fields/#filefield>`_
                                that references the actual kml
        ======================  ==============================================
    """    
    
    creation_date = models.DateTimeField(auto_now=True) 
    
    active = models.BooleanField(default=True, help_text="""
        Checking here indicates that this layer list should be the one used in
        the application. Copies of other layer lists are retained in the
        system so you can go back to an old version if necessary.
    """)
    
    kml = models.FileField(upload_to='layers/uploaded-kml/', help_text="""
        KML file that represents the public layers list. This file can use
        NetworkLinks pointing to remote kml datasets or WMS servers.
        For more information on how to create this kml file see the 
        documentation.
    """, blank=False, max_length=510)
    
    def __unicode__(self):
        return "PublicFishingLayer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(PublicFishingLayer, self).save(*args, **kwargs)
        if self.active and PublicFishingLayer.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated
            # There can be only one!
            PublicFishingLayer.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
    '''            
    class Meta:
        permissions = (
            ("view_ecotrustlayerlist", "Can view ecotrust data layer list"),
        )
        db_table = 'layers_ecotrustlayerlist'
    '''    