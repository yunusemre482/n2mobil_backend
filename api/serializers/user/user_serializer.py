from rest_framework import serializers
from api.models.user import Geo, Address, Company, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 3

    @staticmethod
    def create(validated_data):
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')

        geo_data = address_data.pop('geo')
        geo_instance = Geo.objects.create(**geo_data)

        address = Address.objects.create(geo=geo_instance, **address_data)
        company = Company.objects.create(**company_data)

        user_instance = User.objects.create(address=address, company=company, **validated_data)
        return user_instance

    @staticmethod
    def update(instance, validated_data):
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')

        geo_data = address_data.pop('geo')
        geo_instance = Geo.objects.create(**geo_data)

        address = Address.objects.create(geo=geo_instance, **address_data)
        company = Company.objects.create(**company_data)

        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.website = validated_data.get('website', instance.website)
        instance.address = address
        instance.company = company
        instance.save()
        return instance

