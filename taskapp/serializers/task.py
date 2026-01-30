import random

from rest_framework import serializers

from taskapp.models import TaskModel


def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class TaskSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        iterations = 0
        color = get_random_color()
        while self.Meta.model.objects.filter(color=color).exists() and iterations < 5:
            color = get_random_color()
            iterations += 1

        validated_data['color'] = color
        validated_data['user'] = self.context['request'].user
        return super(TaskSerializer, self).create(validated_data)

    class Meta:
        model = TaskModel
        fields = ('id', 'name', 'description', 'category', 'status', 'color')
