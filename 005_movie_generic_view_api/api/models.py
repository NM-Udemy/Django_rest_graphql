from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}({self.year})'

class MovieRating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating')
    average_star = models.FloatField(default=0)

class Role(models.Model):
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='roles')
    
    def __str__(self):
        return f"{self.movie}: {self.name}"


class Staff(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(default=None)
    roles = models.ManyToManyField(Role, related_name='staffs')
    
    def __str__(self):
        return f'{self.name} ({self.birthday})'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    star = models.IntegerField()
    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        average_star = Comment.objects.filter(movie=self.movie).aggregate(models.Avg('star')).get('star__avg')
        MovieRating.objects.update_or_create(
            movie=self.movie,
            average_star=average_star
        )