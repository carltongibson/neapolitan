======================
Neapolitan's Templates
======================

Neapolitan provides generic templates that can be used as a starting point for
your project.


``object_form.html``
=====================

Used for both the create and update views.

``neapolitan/object_list.html``

Context variables:

* ``object``: the object being updated, if present.
* ``form``: the form.
* ``object_verbose_name``: the verbose name of the object, e.g. ``bookmark``.
* ``create_view_url``: the URL for the create view.
* ``update_view_url``: the URL for the update view.


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
