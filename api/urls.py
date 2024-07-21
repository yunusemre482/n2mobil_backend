from django.urls import path, include
from .routes.user_routes import urlpatterns as user_urls
from .routes.todo_routes import urlpatterns as todo_urls

## add to array of urlpatterns
urlpatterns = [
    path('', include(user_urls)),
    path('', include(todo_urls))
]


