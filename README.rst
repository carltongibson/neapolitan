==========
Neapolitan
==========

.. image:: https://img.shields.io/pypi/v/neapolitan.svg
  :target: https://pypi.org/project/neapolitan/
  :alt: PyPI version

I have a Django model:

.. code:: python

    from django.db import models

    class Bookmark(models.Model):
        url = models.URLField(unique=True)
        title = models.CharField(max_length=255)
        note = models.TextField(blank=True)
        favourite = models.BooleanField(default=False)

I want easy CRUD views for it, without it taking all day:

.. code:: python

    # urls.py
    from neapolitan.views import CRUDView
    from .models import Bookmark

    class BookmarkView(CRUDView):
        model = Bookmark
        fields = ["url", "title", "note"]
        filterset_fields = [
            "favourite",
        ]

    urlpatterns = [
        *BookmarkView.get_urls(),
    ]

Neapolitan's ``CRUDView`` provides the standard list, detail,
create, edit, and delete views for a model, as well as the hooks you need to
be able to customise any part of that.

Neapolitan provides base templates and re-usable template tags to make getting
your model on the page as easy as possible.

Where you take your app after that is up to you. But Neapolitan will get you
started.

Let's go! 🚀

Next stop `the docs <https://noumenal.es/neapolitan/>`_ 🚂

Versioning and Status
---------------------

Neapolitan uses a two-part CalVer versioning scheme, such as ``23.7``. The first
number is the year. The second is the release number within that year.

This is alpha software. I'm still working out the details of the API, and I've
only begun the docs.

**But**: You could just read ``neapolitan.views.CRUDView`` and see what it does.
Up to you. 😜

Installation
------------

Install with pip:

.. code:: bash

    pip install neapolitan

Add ``neapolitan`` to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        ...
        "neapolitan",
    ]

Templates expect a ``base.html`` template to exist and for that to defined a
``content`` block. (Refs <https://github.com/carltongibson/neapolitan/issues/6>.)
