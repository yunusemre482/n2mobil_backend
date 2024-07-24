from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.album import AlbumViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='user-albums')


urlpatterns = [
    path('', include(router.urls)),
]