==================
CRUDView Reference
==================

.. py:currentmodule:: neapolitan.views

.. autoclass:: CRUDView

Request Handlers
================

The core of a class-based view are the request handlers — methods that convert an HTTP request into a response. The request handers are the essence of the **view**.

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






Other Methods
=============

.. automethod:: CRUDView.get_context_data

  .. literalinclude:: ../../src/neapolitan/views.py
    :pyobject: CRUDView.get_context_data
