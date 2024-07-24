from rest_framework import serializers
from api.models.photo_model import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('album.py',)

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    @staticmethod
    def update(instance, validated_data, **kwargs):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.thumbnail_url = validated_data.get('thumbnail_url', instance.thumbnail_url)

        ## save the kwargs to the instance
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
        return instance
