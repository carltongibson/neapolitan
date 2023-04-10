==========
Neapolitan
==========

I have a Django model::

    from django.db import models

    class Bookmark(models.Model):
        url = models.URLField(unique=True)
        title = models.CharField(max_length=255)
        note = models.TextField(blank=True)
        favourite = models.BooleanField(default=False)

I want easy CRUD views for it, without it taking all day::

    # urls.py
    from neapolitan.views import CRUDView

    class BookmarkView(CRUDView):
        model = Bookmark
        fields = ["url", "title", "note"]
        filterset_fields = [
            "favourite",
        ]

    urlpatterns = [ ... ] + BookmarkView.get_urls()

Neapolitan's ``CRUDView`` provides the standard list, detail,
create, edit, and delete views for a model, as well as the hooks you need to
be able to customise any part of that.

Neapolitan provides base templates and re-usable template tags to make getting
your model on the page as easy as possible.

Where you take your app after that is up to you. But Neapolitan will get you
started.

Let's go! 🚀

Status
------

This is alpha software. I'm still working out the details of the API, and I've
not written the docs.

**But**: You could just read `neapolitan.views.CRUDView` and see what it does.
Up to you. 😜

Installation
------------

Install with pip::

    pip install neapolitan

Add ``neapolitan`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        "neapolitan",
    ]

Templates expect a ``base.html`` template to exist and for that to defined a
``content`` block. (Refs <https://github.com/carltongibson/neapolitan/issues/6>.)
