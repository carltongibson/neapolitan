Neapolitan
==========

Neapolitan is a re-usable library for Django projects, that provides quick CRUD views
for other applications.

It helps you get your models into your web output as quickly as possible, and includes base
templates and re-usable template tags.

All kinds of applications need frontend CRUD functionality - but it's not available out of
the box with Django, and Python programmers often suffer while wrestling with the unfamiliar
technologies and tools required to implement it. Neapolitan addresses that particular
headache.

If you've ever looked longingly at Django's admin functionality and wished you could have
the same kind of CRUD access that it provides for your frontend, then Neapolitan is for you.


Contents
--------

.. toctree::
    :maxdepth: 1

    tutorial
    crud-view
    templates


A quick look
------------

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

Read the :ref:`tutorial` for a step-by-step guide to getting it up and running. Let's go! 🚀


Contribute!
-----------

Neapolitan is very much under construction 🚧.

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

A quick introductory talk
-------------------------

My DjangoCon Europe talk from 2023 was about Neapolitan, and how it came to be. It gives a quick introduction, and some of the thinking behind it.

You might want to watch that. 🍿

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/_3oGI4RC52s" title="YouTube video player" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

