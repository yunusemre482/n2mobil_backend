from django.http import Http404
from django.shortcuts import get_object_or_404
from filter_and_pagination import FilterPagination
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from api.models import Album, Photo
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsPublic
from api.serializers import AlbumSerializer, PhotoSerializer

import logging

logger = logging.getLogger(__name__)


class AlbumViewSet(viewsets.ViewSet):
    serializer_class = AlbumSerializer
    photo_serializer_class = PhotoSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['list', 'create']:
            permission_classes = [IsPublic]
        elif self.action in ['update', 'partial_update', 'destroy','add_photo', 'get_album_photos']:
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self, request):
        queryset = FilterPagination.filter_and_pagination(request, Album)
        return queryset

    def list(self, request):
        queryset = FilterPagination.filter_and_pagination(request, Album)
        serialize_data = AlbumSerializer(queryset['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': queryset['pagination']}

        return Response(resultset)

    def create(self, request):

        userId = request.user.id if request.user.id else None

        if userId:
            request.data['userId'] = userId

        album_serializer = AlbumSerializer(data=request.data)

        if album_serializer.is_valid():

            album_instance = album_serializer.save()
            serialized_todo = AlbumSerializer(album_instance)
            return Response(serialized_todo.data, status=status.HTTP_201_CREATED)
        else:
            return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise NotFound('Album not found.')
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise NotFound('Album not found.')
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise NotFound('Album not found.')
        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise NotFound('Album not found.')
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='photos')
    def get_album_photos(self, request, pk=None):
        album = get_object_or_404(Album, pk=pk)

        ##add filter data to the queryset here as albumId

        request.query_params._mutable = True

        request.query_params['albumId'] = album.id

        queryset = FilterPagination.filter_and_pagination(request, Photo)

        serialize_data = PhotoSerializer(queryset['queryset'], many=True).data

        result_set = {'dataset': serialize_data, 'pagination': queryset['pagination']}


        return Response(result_set, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-photo')
    def add_photo(self, request, pk=None):
        album = Album.objects.get(pk=pk)

        if not album:
            raise NotFound('Album not found.')

        request.data['albumId'] = album.id

        photo_serializer = PhotoSerializer(data=request.data)

        if photo_serializer.is_valid():
            photo_instance = photo_serializer.save()
            serialized_photo = PhotoSerializer(photo_instance)

            return Response({'message': 'Photo added successfully.','photo': serialized_photo.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Photo can note  add.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='photos/(?P<photo_id>[^/.]+)')
    def delete_photo(self, request, pk=None, photo_id=None):
        photo = Photo.objects.get(pk=photo_id)

        if not photo:
            raise NotFound('Photo not found.')

        photo.delete()
        return Response({'message': 'Photo deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)