from django.db import models

from lingcod.mpa.models import Mpa as BaseMpa
from lingcod.array.models import MpaArray as BaseMpaArray

#if the names of the following two classes are changed, the related settings should also be changed (MPA_CLASS, ARRAY_CLASS)

class Habitat(BaseMpa):
    pass

class MpaArray(BaseMpaArray):
    pass

