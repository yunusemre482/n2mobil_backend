from rest_framework import serializers
from api.models.user import Geo, Address, Company, User
from api.serializers.user.address_serializer import AddressSerializer
from api.serializers.user.company_serializer import CompanySerializer
from django.contrib.auth.hashers import make_password

import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

    ## exculude password from response
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)