from lingcod.mpa.forms import MpaForm as BaseMpaForm
from lingcod.array.forms import ArrayForm as BaseArrayForm
from models import AOI, AOIArray
from django import forms

#if the names of the following two classes are changed, the related settings should also be changed (MPA_FORM, ARRAY_FORM)

class ArrayForm(BaseArrayForm):
    class Meta(BaseArrayForm.Meta):
        model = AOIArray
        exclude = ('sharing_groups',)

class AOIForm(BaseMpaForm):
    name = forms.CharField(label='Area Name')
    class Meta:
        model = AOI
        exclude = ('sharing_groups','content_type','object_id','designation')
