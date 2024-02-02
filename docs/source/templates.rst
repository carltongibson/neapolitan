==================
Template reference
==================

Neapolitan provides generic templates that can be used as a starting point for
your project.

The default templates use TailwindCSS classes, for styling. See the `guide here
for integrating TailwindCSS with Django
<https://noumenal.es/notes/tailwind/django-integration/>`_.

The templates ``{% extends "base.html" %}``, which must provide
``{% block content %}``. Neapolitan may provide a base template in the future,
see `issue #6 <https://github.com/carltongibson/neapolitan/issues/6>`_.

This is the full listing of the provided templates:

.. code-block:: shell

    templates
    └── neapolitan
        ├── object_confirm_delete.html
        ├── object_detail.html
        ├── object_form.html
        ├── object_list.html
        └── partial
            ├── detail.html
            └── list.html

Templates
=========

You can override these templates by creating your own, either individually or as
a whole.

If you want to override a single template for your model, you can run the ``mktemplate``
management command:

.. code-block:: shell

    python manage.py mktemplate myapp.MyModel --list

You pass your model in the ``app_name.ModelName`` format, and then an option for the
CRUD template you want to override. The specified template will be copied to your app's
``templates``, using your active neapolitan default templates, and having the correct
name applied.

For example, the above command will copy the active ``neapoltian/object_list.html`` template to your app's
``templates/myapp/mymodel_list.html``, where it will be picked up by a ``CRUDView`` for
``MyModel`` when serving the list view.

See ``python manage.py mktemplate --help`` for full details.


.. admonition:: Under construction 🚧

    The templates are still being developed. If a change in a release affects
    you, you can copy the templates from the previous version to continue, but
    please also an open an issue to discuss.


``object_form.html``
--------------------

Used for both the create and update views.

``neapolitan/object_list.html``

Context variables:

* ``object``: the object being updated, if present.
* ``object_verbose_name``: the verbose name of the object, e.g. ``bookmark``.
* ``form``: the form.
* ``create_view_url``: the URL for the create view.
* ``update_view_url``: the URL for the update view.

``object_confirm_delete.html``
------------------------------

Used for the delete view.

``neapolitan/object_confirm_delete.html``

Context variables:

* ``object``: the object being deleted.
* ``object_verbose_name``: the verbose name of the object, e.g. ``bookmark``.
* ``form``: the form.
* ``delete_view_url``: the URL for the delete view.


Template tags
=============

.. currentmodule:: neapolitan.templatetags.neapolitan

Neapolitan provides template tags for generic object and object list rendering.

Assuming you have ``neaopolitan`` in your ``INSTALLED_APPS`` setting, you can
load the tags as usual with:

.. code-block:: html+django

    {% load neapolitan %}


``object_detail``
-----------------

.. autofunction:: object_detail


``object_list``
---------------

.. autofunction:: object_list
