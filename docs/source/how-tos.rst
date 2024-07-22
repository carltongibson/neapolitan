=======
How Tos
=======


Project-level Overrides
=======================

Maybe ``CRUDView`` doesn't work exactly how you want. Maybe you need to
override something whilst experimenting.

You can add a base-class of your own to add project-level overrides.

In your ``views.py``::

    from neapolitan.views import CRUDView as BaseCRUDView


    class CRUDView(BaseCRUDView):
        # Add your overrides here.


    class MyModelCRUDView(CRUDView):
        model = "MyModel"
        fields = ["name", "description"]

By defining your base-class like this, you can revert to Neapolitan's class
simply by commenting it out, or deleting it, and adjusting the import.
