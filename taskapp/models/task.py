import random

from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import BaseModel


def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class StatusChoices(models.TextChoices):
    BACKLOG = 'BACKLOG', _('Backlog')
    TODO = 'TODO', _('To Do')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    REVIEW = 'REVIEW', _('Review')
    BLOCKED = 'BLOCKED', _('Blocked')
    DONE = 'DONE', _('Done')
    CANCELLED = 'CANCELLED', _('Cancelled')

class TaskModel(BaseModel):
    name = models.CharField(_('name'), max_length=100, blank=False)
    description = models.TextField(_('description'), blank=True)
    category = models.ForeignKey('CategoryModel', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=StatusChoices.choices, default=StatusChoices.BACKLOG)
    color = ColorField(_('color'), max_length=7, default='', blank=True)

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'