from lingcod.features.forms import FeatureForm, SpatialFeatureForm
from models import AOI, AOIArray, UserKml
from django import forms

#if the names of the following two classes are changed, the related settings should also be changed (MPA_FORM, ARRAY_FORM)

class ArrayForm(FeatureForm):
    name = forms.CharField(label='AOI Group Name')
    class Meta(FeatureForm.Meta):
        model = AOIArray

class AOIForm(SpatialFeatureForm):
    name = forms.CharField(label='Area Name')
    class Meta(SpatialFeatureForm.Meta):
        model = AOI

class UserKmlForm(FeatureForm):
    class Meta(FeatureForm.Meta):
        model = UserKml
