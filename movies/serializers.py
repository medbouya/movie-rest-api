from rest_framework import serializers

from .models import Movie, Comment


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'plot', 'director', 'year', 'poster']
        # Excluding fields from the form that allow creating movies
        read_only_fields = ['plot', 'director', 'year', 'poster']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'movie']
