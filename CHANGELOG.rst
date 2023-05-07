=========
CHANGELOG
=========

Neapolitan is still in **alpha** stage. It won't change much but I'm still
working out the fine details of the API.

The provided templates (in particular) will evolve as needed without notice
until we get closer to a resting place. If a change affects you, you can copy to
templates as were to your own project, and go from there.

Version numbers correspond to git tags. Please use the compare view on GitHub
for full details. Until we're further along, I will just note the highlights
here:

23.10
=====

* Added a ``{{ delete_view_url}}`` context variable for the form action to the
  ``object_confirm_delete.html`` template.
* Added basic styling and docs for the ``object_confirm_delete.html`` template.

23.9
====

Adds the beginnings of some TailwindCSS styling to the provided templates. See
the `guide here for integrating TailwindCSS with Django
<https://noumenal.es/notes/tailwind/django-integration/>`_.

* These are merely CSS classes, so you can ignore them, or override the
  templates if you're not using Tailwind.

* The templates docs now have an introductory sections about the templates to
  give a bit of guidance there.

The ``<form>`` element in the ``object_form.html`` template has a ``.dl-form``
class applied, to go with the styles used in the ``object_detail.html``.

* This assumes you're using Django's new div-style form rendering.

* This needs a Tailwind plugin to be applied, which is still under-development.
  Please see see `issue #8
  <https://github.com/carltongibson/neapolitan/issues/8>`_ for an example
  snippet that you can add to your Tailwind configuration now.

23.8
====

* Adjusted object-view action links to include the detail view link.

23.7
====

To 23.7: initial exploratory work.
