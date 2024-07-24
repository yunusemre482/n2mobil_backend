from filter_and_pagination import FilterPagination
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from api.models import Post, Comment
from api.permissions import IsPublic, IsLoggedInUserOrAdmin
from api.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    comment_serializer_class = CommentSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['list', 'create']:
            permission_classes = [IsPublic]
        elif self.action in ['update', 'partial_update', 'destroy', 'get_post_comments', 'add_comment', 'delete_comment']:
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def list(self, request):
        queryset = FilterPagination.filter_and_pagination(request, Post)
        serialize_data = PostSerializer(queryset['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': queryset['pagination']}

        return Response(resultset)

    def create(self, request, *args, **kwargs):
        userId = request.user.id if request.user.id else None

        if not userId:
            return Response({'error': 'You must be logged in to create a post.'}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['userId'] = userId

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
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

    @action(detail=True, methods=['get'], url_path='comments')
    def get_post_comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        ##add filter data to the queryset here as albumId
        request.query_params._mutable = True

        request.query_params['postId'] = post.id

        queryset = FilterPagination.filter_and_pagination(request, Comment)

        serialize_data = CommentSerializer(queryset['queryset'], many=True).data

        result_set = {'dataset': serialize_data, 'pagination': queryset['pagination']}

        return Response(result_set, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-comment')
    def add_comment(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        request.data['postId'] = post.id

        comment_serializer = CommentSerializer(data=request.data)

        if comment_serializer.is_valid():
            comment_instance = comment_serializer.save()
            serialized_comment = CommentSerializer(comment_instance)

            return Response({'message': 'Comment added successfully.', 'photo': serialized_comment.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Comment can not created !'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)')
    def delete_comment(self, request, pk=None, comment_id=None):
        commet = Comment.objects.get(pk=comment_id)

        if not commet:
            raise NotFound('Comment not found.')

        commet.delete()

        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)