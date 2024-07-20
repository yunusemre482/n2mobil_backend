from rest_framework import serializers
from api.models.user import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.street = validated_data.get('street', instance.street)
        instance.suite = validated_data.get('suite', instance.suite)
        instance.city = validated_data.get('city', instance.city)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.geo = validated_data.get('geo', instance.geo)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'street': instance.street,
            'suite': instance.suite,
            'city': instance.city,
            'zipcode': instance.zipcode,
            'geo': instance.geo
        }

    def to_internal_value(self, data):
        return {
            'street': data['street'],
            'suite': data['suite'],
            'city': data['city'],
            'zipcode': data['zipcode'],
            'geo': data['geo']
        }

