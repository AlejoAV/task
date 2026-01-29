from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import BaseModel

class CategoryModel(BaseModel):
    name = models.CharField(_('name'), max_length=100, blank=False)
    description = models.TextField(_('description'), blank=True)
