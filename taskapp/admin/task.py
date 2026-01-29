from django.contrib import admin

from taskapp.models import TaskModel


# Register your models here.

@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    pass