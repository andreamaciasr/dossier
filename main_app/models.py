from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("saved_articles")


class Article(models.Model):
    headline = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
