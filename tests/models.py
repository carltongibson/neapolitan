from django.db import models


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    favourite = models.BooleanField(default=False)
