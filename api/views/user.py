from django.http import Http404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.models.user import User
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsPublic
from api.serializers import UserSerializer, AddressSerializer, CompanySerializer, PostSerializer, AlbumSerializer, \
    TodoSerializer
from filter_and_pagination import FilterPagination

import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['create', 'list']:
            permission_classes = [IsPublic]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self, request):
        queryset = FilterPagination.filter_and_pagination(request, User)
        return queryset

    def create(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_data = user_serializer.validated_data

            address_data = user_data.pop('address', None)
            company_data = user_data.pop('company', None)

            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address_instance = address_serializer.save()
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            company_serializer = CompanySerializer(data=company_data)
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_instance = User.objects.create(
                address=address_instance,
                company=company_instance,
                **user_data
            )

            serialized_user = UserSerializer(user_instance)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset(request)

        queryset = FilterPagination.filter_and_pagination(request, User)
        serialize_data = UserSerializer(queryset['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': queryset['pagination']}

        return Response(resultset)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            raise NotFound('User not found.')
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'User deleted successfully.'})

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        posts = user.post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        albums = user.album_set.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def todos(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        todos = user.todo_set.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
