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

        staus = models.CharField(
            max_length=2,
            choices=STATUS_CHOICES,
        )

        last_review = models.DateField(null=True, blank=True)

        def is_at_risk(self):
            return self.status in {self.BLOCKED, self.INACTIVE}

        def __str__(self):
            return self.question_text



Then add the project, the ``projects`` module and Neapolitan to the beginning of
``INSTALLED_APPS`` in ``settings.py``:

 .. code-block:: Python
   :emphasize-lines: 2-4

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
``{% extends "base.html" %}`` so you'll have to provide one at ``dashboard/templates/base.html``::

    {% block content %}{% endblock %}


And at the end of ``dashboard/urls.py``::

    from neapolitan.views import CRUDView

    import projects

    class ProjectView(CRUDView):
        model = projects.models.Project
        fields = ["name", "owner", "has_tests", "has_docs", "status"]

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

Next, Tailwind needs to be able to find all Django's templates so it can target them. We'll
achieve this by having Tailwind run a Django management command.

First, create the management command in ``/dashboard/management/commands/list_templates.py``::

    import os

    from django.conf import settings
    from django.core.management.base import BaseCommand
    from django.template.utils import get_app_template_dirs


    class Command(BaseCommand):
        help = "List all template files"

        def handle(self, *args, **options):
            template_files = []
            app_template_dirs = get_app_template_dirs("templates")
            for app_template_dir in app_template_dirs:
                template_files += self.list_template_files(app_template_dir)
            template_files += self.list_template_files(settings.TEMPLATES[0]["DIRS"])

            self.stdout.write("\n".join(template_files))

        def list_template_files(self, template_dir):
            template_files = []
            # TODO: Look into using pathlib.Path.rglob() instead. 🤔
            for dirpath, _, filenames in os.walk(str(template_dir)):
                for filename in filenames:
                    if filename.endswith(".html") or filename.endswith(".txt"):
                        template_files.append(os.path.join(dirpath, filename))
            return template_files

Then, at the root of the ``dashboard`` project, `install the standalone Tailwind CLI
<https://tailwindcss.com/blog/standalone-cli>`_, and run ``init`` to create a default
``tailwind.config.js`` file::

    ./tailwindcss init

You'll need to edit ``tailwind.config.js``, adding::

    const path = require('path');
    const projectRoot = path.resolve(__dirname, '../../..');

    const { spawnSync } = require('child_process');

    // Function to execute the Django management command and capture its output
    const getTemplateFiles = () => {
      const command = 'python'; // Requires virtualenv to be activated.
      const args = ['manage.py', 'list_templates']; // Requires cwd to be set.
      const options = { cwd: projectRoot };
      const result = spawnSync(command, args, options);

      if (result.error) {
        throw result.error;
      }

      if (result.status !== 0) {
        console.log(result.stdout.toString(), result.stderr.toString());
        throw new Error(`Django management command exited with code ${result.status}`);
      }

      const templateFiles = result.stdout.toString()
        .split('\n')
        .map((file) => file.trim())
        .filter(function(e){return e});  // Remove empty strings, including last empty line.
      return templateFiles;
    };

    module.exports = {
      // Allow configuring some folders manually, and then concatenate with the
      // output of the Django management command.
      content: [].concat(getTemplateFiles()),
      theme: {
        extend: {},
      },
      plugins: [],
    }
    // console.log(module.exports)

.. important:: You need to delete the origin ``module.exports`` dictionary.



.. seealso::

    `Integrate TailwindCSS into Django <https://noumenal.es/notes/tailwind/django-integration/>`_.
