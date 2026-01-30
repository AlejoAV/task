from rest_framework import serializers

from taskapp.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id','name','description')