from filter_and_pagination import FilterPagination
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from api.models import Todo
from api.permissions import IsPublic, IsLoggedInUserOrAdmin
from api.serializers import TodoSerializer
import logging

logger = logging.getLogger(__name__)


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    # NOTE: This is the permission class that will be used to check if the user is authenticated or not before performing any action
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['create', 'list']:
            permission_classes = [IsPublic]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self, request):
        queryset = FilterPagination.filter_and_pagination(request, Todo)
        return queryset

    def create(self, request):
        logger.warning(f"request.user: {request.user.id}")
        userId = request.user.id if request.user.id else None

        logger.warning(f"user id from request: {request.user.id}")

        if userId:
            request.data['userId'] = userId

        logger.warning(f"request.data: {request.data}")

        todo_serializer = TodoSerializer(data=request.data)


        if todo_serializer.is_valid():
            todo_instance = todo_serializer.save()
            serialized_todo = TodoSerializer(todo_instance)
            return Response(serialized_todo.data, status=status.HTTP_201_CREATED)
        else:
            return Response(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = FilterPagination.filter_and_pagination(request, Todo)
        serialize_data = TodoSerializer(queryset['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': queryset['pagination']}

        return Response(resultset)

    @action(detail=False, methods=['get'], url_path='user-todos')
    def list_user_todos(self, request):
        queryset = Todo.objects.filter(userId=request.user.id)
        serialize_data = TodoSerializer(queryset, many=True).data
        return Response(serialize_data)

    def retrieve(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound('Todo not found.')
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound('Todo not found.')
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound('Todo not found.')
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound('Todo not found.')
        todo.delete()
        return Response({'message': 'Todo deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed(self, request):
        queryset = Todo.objects.filter(user=request.user, completed=True)
        serialize_data = TodoSerializer(queryset, many=True).data
        return Response(serialize_data)

    @action(detail=False, methods=['get'], url_path='incomplete')
    def incomplete(self, request):
        queryset = Todo.objects.filter(user=request.user, completed=False)
        serialize_data = TodoSerializer(queryset, many=True).data
        return Response(serialize_data)

    @action(detail=True, methods=['patch'], url_path='toggle')
    def toggle(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound('Todo not found.')
        todo.completed = not todo.completed
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='toggle-all')
    def toggle_all(self, request):
        completed = request.data.get('completed', False)
        Todo.objects.filter(user=request.user).update(completed=completed)
        queryset = self.get_queryset()
        serialize_data = TodoSerializer(queryset, many=True).data
        return Response(serialize_data)
