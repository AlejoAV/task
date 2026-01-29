from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True, null=True)
    enable = models.BooleanField(_('enable'), default=True, blank=True)

    class Meta:
        abstract = True
