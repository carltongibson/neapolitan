import uuid
from django.db import models


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    favourite = models.BooleanField(default=False)


class NamedCollection(models.Model):
    """For testing UUID lookup"""
    name = models.CharField(max_length=25, unique=True)
    code = models.UUIDField(unique=True, default=uuid.uuid4)
