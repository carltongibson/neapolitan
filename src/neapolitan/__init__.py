"""
Neapolitan: quick CRUD views for Django.

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

Neapolitan's `CRUDView` provides the standard list, detail,
create, edit, and delete views for a model, as well as the hooks you need to
be able to customise any part of that.

Neapolitan provides base templates and re-usable template tags to make getting
your model on the page as easy as possible.

Where you take your app after that is up to you. But Neapolitan will get you
started.

Let's go! 🚀
"""

__version__ = "24.4"
