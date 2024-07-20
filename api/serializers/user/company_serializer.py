from rest_framework import serializers

from api.models.user import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

    def to_representation(self, instance):
        return {
            'name': instance.name
        }

    def to_internal_value(self, data):
        return {
            'name': data['name']
        }

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
