from django.contrib import admin

from taskapp.models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    pass