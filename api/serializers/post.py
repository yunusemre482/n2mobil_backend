from rest_framework import serializers
from api.models.post_model import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    @staticmethod
    def update(instance, validated_data, **kwargs):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.published = validated_data.get('published', instance.published)

        ## save the kwargs to the instance
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
        return instance
