from rest_framework import serializers
from api.models.user import Geo


class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = ['lat', 'lng']

    def to_representation(self, instance):
        return {
            'lat': instance.lat,
            'lng': instance.lng
        }

    def to_internal_value(self, data):
        return {
            'lat': data['lat'],
            'lng': data['lng']
        }

    def create(self, validated_data):
        return Geo.objects.create(**validated_data)
