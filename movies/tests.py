import json
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from django.urls import reverse
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer


# initialize the APIClient app
client = Client()


# Movie Tests
class GetMoviesTest(TestCase):
    """ Test module for GET all movies API """

    def setUp(self):
        Movie.objects.create(
            title='The Social Network', plot='...', director='...', year=2010, poster='http://something1.com',)
        Movie.objects.create(
            title='', plot='...', director='...', year=2010, poster='http://something2.com',)
        Movie.objects.create(
            title='Jobs', plot='...', director='...', year=2013, poster='http://something3.com',)
        Movie.objects.create(
            title='Imitation Game', plot='...', director='...', year=2014, poster='http://something4.com',)

    def test_get_movies(self):
        # get API response
        response = client.get(reverse('movies'))
        # get data from db
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleMovieTest(TestCase):
    """ Test module for GET single movie API """

    def setUp(self):
        self.movie1 = Movie.objects.create(
            title='The Social Network', plot='...', director='...', year=2010, poster='http://something1.com',)
        self.movie2 = Movie.objects.create(
            title='', plot='...', director='...', year=2010, poster='http://something2.com',)
        self.movie3 = Movie.objects.create(
            title='Jobs', plot='...', director='...', year=2013, poster='http://something3.com',)
        self.movie4 = Movie.objects.create(
            title='Imitation Game', plot='...', director='...', year=2014, poster='http://something4.com',)

    def test_get_valid_single_movie(self):
        response = client.get(
            reverse('movie-detail', kwargs={'pk': self.movie3.pk}))
        movie = Movie.objects.get(pk=self.movie3.pk)
        serializer = MovieSerializer(movie)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_movie(self):
        try:
            response = client.get(
                reverse('movie-detail', kwargs={'pk': 30}))
            status_code = response.status_code
        except Movie.DoesNotExist:
            status_code = 404

        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)


class CreateNewMovieTest(TestCase):
    """ Test module for POST single movie API """

    def setUp(self):
        self.valid_payload = {
            'title': 'Jobs',
            'plot': '...',
            'director': '...',
            'year': 2022,
            'poster': 'https://something1.com'

        }
        self.invalid_payload = {
            'title': '',
            'plot': '...',
            'director': '...',
            'year': 2022,
            'poster': 'https://something1.com'
        }

    def test_create_valid_movie(self):
        response = client.post(
            reverse('movies'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_movie(self):
        response = client.post(
            reverse('movies'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Comment Tests
class GetCommentsTest(TestCase):
    """ Test module for GET all comments API """

    def setUp(self):
        self.movie1 = Movie.objects.create(
            title='The Social Network', plot='...', director='...', year=2010, poster='http://something1.com',)
        self.movie2 = Movie.objects.create(
            title='', plot='...', director='...', year=2010, poster='http://something2.com',)
        self.movie3 = Movie.objects.create(
            title='Jobs', plot='...', director='...', year=2013, poster='http://something3.com',)
        self.movie4 = Movie.objects.create(
            title='Imitation Game', plot='...', director='...', year=2014, poster='http://something4.com',)

        Comment.objects.create(
            text='A comment', movie=self.movie1)
        Comment.objects.create(
            text='A comment', movie=self.movie2)
        Comment.objects.create(
            text='A comment', movie=self.movie3)
        Comment.objects.create(
            text='A comment', movie=self.movie4)

    def test_get_comments(self):
        # get API response
        response = client.get(
            reverse('comments'))

        # Initiating APIRequestFactory and getting all comments
        factory = APIRequestFactory()
        request = factory.get('comments')

        # Setting up the request in order to pass it to the CommentSerializer as a context
        serializer_context = {
            'request': Request(request),
        }

        # get data from db
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, context=serializer_context, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMovieCommentsTest(TestCase):
    """ Test module for GET all comment for a single movie movie API """

    def setUp(self):
        self.movie = Movie.objects.create(
            title='The Social Network', plot='...', director='...', year=2010, poster='http://something1.com',)

        Comment.objects.create(
            text='A comment', movie=self.movie)
        Comment.objects.create(
            text='A comment', movie=self.movie)
        Comment.objects.create(
            text='A comment', movie=self.movie)
        Comment.objects.create(
            text='A comment', movie=self.movie)

    def test_get_valid_single_movie(self):

        # Initiating APIRequestFactory and getting all comments
        factory = APIRequestFactory()
        request = factory.get('comments')

        # Setting up the request in order to pass it to the CommentSerializer as a context
        serializer_context = {
            'request': Request(request),
        }

        response = client.get(
            reverse('comments-movie', kwargs={'movie_id': self.movie.pk}))
        comments = Comment.objects.filter(movie__id=self.movie.pk)
        serializer = CommentSerializer(
            comments, context=serializer_context, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_movie(self):
        response = client.get(
            reverse('comments-movie', kwargs={'movie_id': 30}))
        comments = Comment.objects.filter(movie_id=30)
        # checking if the Queryset is empty
        if not comments:
            response.status_code = 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCommentTest(TestCase):
    """ Test module for POST single comment API """

    def setUp(self):

        self.movie = Movie.objects.create(
            title='The Social Network', plot='...', director='...', year=2010, poster='http://something1.com',)

        self.valid_payload = {
            'text': 'My comment',
            'movie': reverse('movie-detail', kwargs={'pk': self.movie.pk}),
        }
        self.invalid_payload = {
            'text': '',
            'movie': 'M',
        }

    def test_create_valid_comment(self):
        response = client.post(
            reverse('comments'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_comment(self):
        response = client.post(
            reverse('comments'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
