from rest_framework import serializers
from .geo_serializer import GeoSerializer
from ...models.user import Address, Geo


class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = '__all__'


    def create(self, validated_data):
        geo_data = validated_data.pop('geo')
        geo = Geo.objects.create(**geo_data)
        address = Address.objects.create(geo=geo, **validated_data)
        return address

    def update(self, instance, validated_data):
        geo_data = validated_data.pop('geo')
        geo = instance.geo

        instance.street = validated_data.get('street', instance.street)
        instance.suite = validated_data.get('suite', instance.suite)
        instance.city = validated_data.get('city', instance.city)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.save()

        geo.lat = geo_data.get('lat', geo.lat)
        geo.lng = geo_data.get('lng', geo.lng)
        geo.save()

        return instance

    def to_representation(self, instance):
        # remove address id from response
        response = super().to_representation(instance)
        response.pop('id')
        response['geo'] = GeoSerializer(instance.geo).data

        return response