from django.db import models
from django.contrib.auth.models import User

CATEGORY = (
    ('G', 'General'),
    ('S', 'Science'),
    ('C', 'Culture'),
    ('G', 'Geopolitics'),
    ('E', 'Environment'),
    ('M', 'Middle East'),
    ('P', 'Palestine'),
    ('L', 'Latin America'),
    ('A', 'Africa'),
    ('U', 'US Politics'),
    ('S', 'Asia'),
    ('X', 'Economics'),
)

class Article(models.Model):
    headline = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    category = models.CharField(
    max_length=1,
    choices=CATEGORY,
    default=CATEGORY[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


