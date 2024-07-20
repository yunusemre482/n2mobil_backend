from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet

router = SimpleRouter()

router.register(r'', UserViewSet.as_view(), basename='user')

urlpatterns = router.urls
