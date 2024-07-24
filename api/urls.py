from django.urls import path, include
from .routes.user_routes import urlpatterns as user_urls
from .routes.todo_routes import urlpatterns as todo_urls
from .routes.album_routes import urlpatterns as album_urls
from .routes.post_routes import urlpatterns as post_urls

## add to array of urlpatterns
urlpatterns = [
    path('', include(user_urls)),
    path('', include(todo_urls)),
    path('', include(album_urls)),
    path('', include(post_urls))
]
