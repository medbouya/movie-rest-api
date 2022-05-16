from django.urls import path
from .views import ListCreateMovie, RetrieveUpdateMovie, ListCreateComment, CommentsByMovieList

# define the urls
urlpatterns = [
    path('movies', ListCreateMovie.as_view(), name='movies'),
    path('movies/<pk>', RetrieveUpdateMovie.as_view(), name='movie-detail'),
    path('comments', ListCreateComment.as_view(), name='comments'),
    path('comments/<movie_id>', CommentsByMovieList.as_view(), name='comments-movie'),
]
