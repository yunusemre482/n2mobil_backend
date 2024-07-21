from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import Post
from api.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serialize_data = PostSerializer(queryset, many=True).data
        return Response(serialize_data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Post not found.')
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Post not found.')
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Post not found.')
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Post not found.')
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=True, methods=['get'], url_path='comments')
    # def comments(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         raise NotFound('Post not found.')
    #     comments = post.comment_set.all()
    #     serializer = CommentSerializer(comments, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=True, methods=['post'], url_path='comments')
    # def add_comment(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         raise NotFound('Post not found.')
    #     serializer = CommentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(post=post)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

