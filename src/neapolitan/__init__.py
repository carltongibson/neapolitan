"""
Neapolitan

I have a Django model::

    from django.db import models

    class Bookmark(models.Model):
        url = models.URLField(unique=True)
        title = models.CharField(max_length=255)
        note = models.TextField(blank=True)

I want easy CRUD views for it, without it taking all day::

    # urls.py
    from neapolitan.views import CRUDView

    class BookmarkView(CRUDView):
        model = Bookmark
        fields = ["url", "title", "note"]


    urlpatterns = [ ... ] + BookmarkView.get_urls()

Let's go! 🚀
"""

__version__ = "23.1"
