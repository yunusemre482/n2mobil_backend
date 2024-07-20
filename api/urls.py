from django.urls import path, include
from .routes import user_urls

urlpatterns = [
    path('users/', include(user_urls)),
    #path('users/posts/', include(post.urls)),
    #path('users/albums/', include(album.urls)),
    #path('users/todos/', include(todo.urls)),
    #path('posts/<int:postId>/comments/', include(comment.urls)),
    #path('albums/<int:albumId>/photos/', include(photo.urls))
]