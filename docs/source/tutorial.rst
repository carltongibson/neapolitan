.. _tutorial:

Tutorial
=========

This tutorial will walk you through an example that introduces key operations and
concepts in Neapolitan. It assumes basic familiarity with Django.

The tutorial will build a dashboard for a set of software projects.

Prepare a new Django project
----------------------------

With Django installed, start a new Django project (in a virtual environment, preferably)::

    django-admin startproject dashboard

In the new project directory, create a ``projects`` application::

    python manage.py startapp projects

In ``projects/models.py``, define a ``Project``::

    class Project(models.Model):
        name = models.CharField(max_length=200)
        has_tests = models.BooleanField()
        has_docs = models.BooleanField()

and add the project, the ``projects`` module and Neapolitan to the beginning of
 ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = [
        'projects',
        'neapolitan',
        'dashboard',
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
``{% extends "base.html" %}`` so you'll have to provide one at ``dashboard/templates/
base.html``::

    {% block content %}{% endblock %}


And at the end of ``dashboard/urls.py``::

    from neapolitan.views import CRUDView

    import projects

    class ProjectView(CRUDView):
        model = projects.models.Project
        fields = ["name", "has_tests", "has_docs"]

    urlpatterns += ProjectView.get_urls()

At this point, you can see Neapolitan in action at ``/project/`` (e.g.
http://127.0.0.1:8000/project/). It won't look very beautiful, but you'll see
a table of objects and their attributes, along with options to change their values.


Next steps
----------

The default templates use TailwindCSS classes, for styling. You will need to `integrate TailwindCSS into Django
<https://noumenal.es/notes/tailwind/django-integration/>`_.
