from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api.models.user import User
from api.serializers import UserSerializer, PostSerializer, AlbumSerializer, TodoSerializer


class UserViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['get'])
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        posts = user.post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        albums = user.album_set.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def todos(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        todos = user.todo_set.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
