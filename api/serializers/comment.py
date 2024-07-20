from rest_framework import serializers
from api.models.comment_model import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    @staticmethod
    def update(instance, validated_data, **kwargs):
        instance.body = validated_data.get('body', instance.body)

        ## save the kwargs to the instance
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
        return instance
