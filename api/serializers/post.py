from rest_framework import serializers
from api.models.post_model import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

