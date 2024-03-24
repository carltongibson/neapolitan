==================
CRUDView Reference
==================

.. py:currentmodule:: neapolitan.views

.. autoclass:: CRUDView

Request Handlers
================

The core of a class-based view are the request handlers — methods that convert an HTTP request into an HTTP response. The request handlers are the essence of the **Django view**.

Neapolitan's ``CRUDView`` provides handlers the standard list, detail, create, edit, and delete views for a model.

List and Detail Views
----------------------

.. automethod:: CRUDView.list

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.list

.. automethod:: CRUDView.detail

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.detail

Create and Update Views
-----------------------

.. automethod:: CRUDView.show_form

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.show_form

.. automethod:: CRUDView.process_form

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.process_form

Delete View
-----------

.. automethod:: CRUDView.confirm_delete

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.confirm_delete

.. automethod:: CRUDView.process_deletion

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.process_deletion


QuerySet and object lookup
==========================

.. automethod:: CRUDView.get_queryset

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_queryset

.. automethod:: CRUDView.get_object

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_object


Other Methods
=============

.. automethod:: CRUDView.get_context_data

  .. literalinclude:: ../../src/neapolitan/views.py
    :pyobject: CRUDView.get_context_data
