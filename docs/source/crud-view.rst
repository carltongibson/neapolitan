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


Form handling
=============

.. automethod:: CRUDView.get_form_class

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_form_class

.. automethod:: CRUDView.get_form

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_form

.. automethod:: CRUDView.form_valid

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.form_valid

.. automethod:: CRUDView.form_invalid

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.form_invalid

.. automethod:: CRUDView.get_success_url

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_success_url

Pagination and filtering
========================

.. automethod:: CRUDView.get_paginate_by

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_paginate_by

.. automethod:: CRUDView.get_paginator

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_paginator

.. automethod:: CRUDView.paginate_queryset

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.paginate_queryset

.. automethod:: CRUDView.get_filterset

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_filterset

Response rendering
==================

.. automethod:: CRUDView.get_context_object_name

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_context_object_name

.. automethod:: CRUDView.get_context_data

  .. literalinclude:: ../../src/neapolitan/views.py
    :pyobject: CRUDView.get_context_data

.. automethod:: CRUDView.get_template_names

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.get_template_names

.. automethod:: CRUDView.render_to_response

    .. literalinclude:: ../../src/neapolitan/views.py
        :pyobject: CRUDView.render_to_response
