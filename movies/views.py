import requests
import json

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView

from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer

from django.shortcuts import redirect, render

API = 'https://www.omdbapi.com/?i=tt3896198&apikey=6a51d27&t='


def home(request):

    return render(request, 'home.html')


class ListCreateMovie(ListCreateAPIView):
    """
    API endpoint that allows movies to be listed or created.
    """
    serializer_class = MovieSerializer

    # Movie fields used to filter results
    filter_fields = (
        'year',
    )

    def get_queryset(self):
        return Movie.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            print(serializer.validated_data)
            title = serializer.validated_data['title']
            movie_url = f'{API}{title}'
            response = requests.get(movie_url)
            movie_data = json.loads(response.text)
            if movie_data['Response'] == 'True':
                plot = movie_data['Plot']
                director = movie_data['Director']
                year = int(movie_data['Year'])
                poster = movie_data['Poster']
                serializer.save(plot=plot, director=director,
                                year=year, poster=poster)


class RetrieveUpdateMovie(RetrieveUpdateAPIView):
    """
    API endpoint that allows a movie to be retrieved or updated.
    """
    serializer_class = MovieSerializer

    def get_object(self):
        movie_id = self.kwargs["pk"]
        return Movie.objects.get(id=movie_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListCreateComment(ListCreateAPIView):
    """
    API endpoint that allows comments to be listed or created
    """

    # Comment fields used to filter results
    filter_fields = (
        'movie',
    )

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class CommentsByMovieList(ListAPIView):
    """
    API endpoint that allows to get all comments for a single movie
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        movie_id = self.kwargs["movie_id"]
        return Comment.objects.filter(movie__id=movie_id)
