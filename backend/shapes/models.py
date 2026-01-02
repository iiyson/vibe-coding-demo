from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class ShapeItem(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    shape_type = models.CharField(max_length=50)  # circle, square, triangle
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp", "-id"]
