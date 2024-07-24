from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.album import AlbumViewSet
from api.views.post import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),
]