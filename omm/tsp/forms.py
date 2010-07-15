from lingcod.mpa.forms import MpaForm as BaseMpaForm
from lingcod.array.forms import ArrayForm as BaseArrayForm
from models import Habitat, MpaArray
from django import forms

#if the names of the following two classes are changed, the related settings should also be changed (MPA_FORM, ARRAY_FORM)

class ArrayForm(BaseArrayForm):
    class Meta(BaseArrayForm.Meta):
        model = MpaArray
        exclude = ('sharing_groups',)

class HabitatForm(BaseMpaForm):
    name = forms.CharField(label='Habitat Name')
    class Meta:
        model = Habitat
        exclude = ('sharing_groups','content_type','object_id','designation')
