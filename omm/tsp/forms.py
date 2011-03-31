from lingcod.features.forms import FeatureForm
from models import AOI, AOIArray, UserKml
from django import forms

#if the names of the following two classes are changed, the related settings should also be changed (MPA_FORM, ARRAY_FORM)

class ArrayForm(FeatureForm):
    name = forms.CharField(label='AOI Group Name')
    class Meta(FeatureForm.Meta):
        model = AOIArray
        exclude = ('sharing_groups',)

class AOIForm(FeatureForm):
    name = forms.CharField(label='Area Name')
    class Meta(FeatureForm.Meta):
        model = AOI
        fields = ('user', 'name', 'description', 'geometry_orig', 'geometry_final', 'manipulators')
        exclude = ('sharing_groups','content_type','object_id','designation')

class UserKmlForm(FeatureForm):
    class Meta(FeatureForm.Meta):
        model = UserKml
