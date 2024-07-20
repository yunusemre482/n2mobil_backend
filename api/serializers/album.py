from rest_framework import serializers
from api.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Album.objects.create(**validated_data)

    @staticmethod
    def update(instance, validated_data, **kwargs):
        instance.title = validated_data.get('title', instance.title)

        ## save the kwargs to the instance
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
        return instance
