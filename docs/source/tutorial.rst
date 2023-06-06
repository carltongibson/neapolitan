.. _tutorial:

Tutorial
=========

This tutorial will walk you through an example that introduces key operations and
concepts in Neapolitan. It assumes basic familiarity with Django.

The tutorial will build a dashboard for a set of software projects.

Prepare a new Django project
----------------------------

Install Django and Neapolitan into your environment (a virtual environment, preferably)::

    pip install django neapolitan

Start a new Django project::

    django-admin startproject dashboard

In the new project directory, create a ``projects`` application::

    python manage.py startapp projects

In ``projects/models.py``, define a ``Project``::

    class Project(models.Model):
        name = models.CharField(max_length=200)
        owner = models.CharField(max_length=200)
        has_tests = models.BooleanField()
        has_docs = models.BooleanField()

        NA = "na"
        PLANNED = "PL"
        STARTED = "ST"
        FIRST_RESULTS = "FR"
        MATURE_RESULTS = "MR"
        DONE = "DO"
        DEFERRED = "DE"
        BLOCKED = "BL"
        INACTIVE = "IN"

        STATUS_CHOICES = [
            (PLANNED, "Planned"),
            (STARTED, "Started"),
            (FIRST_RESULTS, "First results"),
            (MATURE_RESULTS, "Mature results"),
            (DONE, "Done"),
            (DEFERRED, "Deferred"),
            (BLOCKED, "Blocked"),
            (INACTIVE, "Inactive"),
        ]

        status = models.CharField(
            max_length=2,
            choices=STATUS_CHOICES,
        )

        last_review = models.DateField(null=True, blank=True)

        def is_at_risk(self):
            return self.status in {self.BLOCKED, self.INACTIVE}

        def __str__(self):
            return self.name



Then add the project, the ``projects`` module and Neapolitan to the beginning of
``INSTALLED_APPS`` in ``settings.py``:

 .. code-block:: Python
   :emphasize-lines: 2-4

    INSTALLED_APPS = [
        'projects',
        'neapolitan',
        [...]
    ]

Create migrations, and run them::

    python manage.py makemigrations
    python manage.py migrate

Wire up the admin; in ``projects/admin.py``::

    from .models import Project

    admin.site.register(Project)

and create a superuser::

    python manage.py createsuperuser

Finally, start the runserver and in the admin, add a few ``Project`` objects to the database.


Wire up Neapolitan views
------------------------

Neapolitan expects to extend a base template (its own templates use
``{% extends "base.html" %}`` so you'll have to provide one at ``dashboard/templates/base.html``::

    {% block content %}{% endblock %}


And at the end of ``dashboard/urls.py``::

    from neapolitan.views import CRUDView

    import projects

    class ProjectView(CRUDView):
        model = projects.models.Project
        fields = ["name", "owner", "last_review", "has_tests", "has_docs", "status"]

    urlpatterns += ProjectView.get_urls()

At this point, you can see Neapolitan in action at ``/project/`` (e.g.
http://127.0.0.1:8000/project/). It won't look very beautiful, but you'll see
a table of objects and their attributes, along with options to change their values
(which will work - you can save changes).


Next steps
----------

The default templates use TailwindCSS classes, for styling. You will need to integrate
TailwindCSS into Django. There is more than one way to do this. The method described here,
from `Tailwind's own documentation <https://tailwindcss.com/docs/installation/play-cdn>`_,
is explicitly *not recommended for production*.

Turn your ``base.html`` into a more complete template, and note the ``<script>`` element:

 .. code-block:: html
   :emphasize-lines: 6

   <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body>
            {% block content %}{% endblock %}
        </body>
    </html>

You notice that the page is now rendered rather more attractively.


.. seealso::

    You can find more detailed information on using Tailwind with Django here: 
    `Integrate TailwindCSS into Django <https://noumenal.es/notes/tailwind/django-integration/>`_.
