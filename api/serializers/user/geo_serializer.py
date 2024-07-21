from rest_framework import serializers
from api.models.user import Geo


class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = ['lat', 'lng']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'lat': representation.get('lat'),
            'lng': representation.get('lng')
        }

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {
            'lat': internal_value.get('lat'),
            'lng': internal_value.get('lng')
        }