from django.db import models

# Create your models here.


class Movie(models.Model):

    title = models.CharField(max_length=256, verbose_name="Title")
    plot = models.TextField(verbose_name="Plot")
    director = models.CharField(max_length=256, verbose_name="Director")
    year = models.PositiveIntegerField(verbose_name="Year")
    poster = models.URLField(max_length=256, unique=True)

    def __str__(self):
        return self.title.capitalize()


class Comment(models.Model):

    text = models.TextField(verbose_name="Comment")
    movie = models.ForeignKey(
        Movie, verbose_name="Movie ID", on_delete=models.CASCADE)
