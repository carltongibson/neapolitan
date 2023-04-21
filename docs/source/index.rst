Welcome to Neapolitan's documentation!
======================================

Neapolitan provides quick CRUD views for Django.

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

Neapolitan's ``CRUDView`` provides the standard list, detail,
create, edit, and delete views for a model, as well as the hooks you need to
be able to customise any part of that.

Neapolitan provides base templates and re-usable template tags to make getting
your model on the page as easy as possible.

Where you take your app after that is up to you. But Neapolitan will get you
started.

Let's go! 🚀


.. toctree::
    :maxdepth: 1
    :caption: Contents:

    crud-view
    templates

.. admonition:: Under construction 🚧

    The docs are still fledging. **But** you can read
    ``neapolitan.views.CRUDView`` to see what it does. (It's just the one
    class!)

    Whilst I'm working on it, if you wanted to make a PR adding a docstring and
    an ``.. automethod::``… you'd be welcome to do so! 🎁

What about the name?
--------------------

It's homage to Tom Christie's
`django-vanilla-views <http://django-vanilla-views.org>`_ which long-ago showed
the way to sanity in regards to class-based views. 🥰 I needed just a little bit
more — filtering, generic templates, auto-routing of multiple views, and that's
about it really — but what's that little bit more than Vanilla?
`Neapolitan <https://en.wikipedia.org/wiki/Neapolitan_ice_cream>`_! 🍨


..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
