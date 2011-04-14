from lingcod.features.forms import FeatureForm, SpatialFeatureForm
from models import AOI, AOIArray, UserKml
from django import forms

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
