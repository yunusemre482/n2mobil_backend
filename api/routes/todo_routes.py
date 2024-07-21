from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.todo import TodoViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='user-todos')


urlpatterns = [
    path('', include(router.urls)),
]