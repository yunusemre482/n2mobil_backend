from rest_framework import serializers
from api.models.todo_model import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
    def create(self, validated_data):
        return Todo.objects.create(**validated_data)

    @staticmethod
    def update(instance, validated_data, **kwargs):
        instance.title = validated_data.get('title', instance.title)
        instance.completed = validated_data.get('completed', instance.completed)

        ## save the kwargs to the instance
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
        return instance