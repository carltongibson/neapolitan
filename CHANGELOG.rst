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

24.4
====

* ``CRUDView`` subclasses may now pass a set of ``roles`` to ``get_urls()`` in
  order to route only a subset of all the available CRUD roles.

  As an example, to route only the list and detail views, the README/Quickstart example
  would become::

    from neapolitan.views import CRUDView, Role
    from .models import Bookmark

    class BookmarkView(CRUDView):
        model = Bookmark
        fields = ["url", "title", "note"]
        filterset_fields = [
            "favourite",
        ]

    urlpatterns = [
        *BookmarkView.get_urls(roles={Role.LIST, Role.DETAIL}),
    ]

  In order to keep this logic within the view here, you would likely override
  ``get_urls()`` in this case, rather than calling it from the outside in your
  URL configuration.

* As well as setting the existing ``lookup_field`` (which defaults to ``"pk"``)
  and ``lookup_url_kwarg`` (which defaults to ``lookup_field`` if not set) you
  may now set ``path_converter`` and ``url_base`` attributes on your
  ``CRUDView`` subclass in order to customise URL generation.

  For example, for this model and ``CRUDView``::

    class NamedCollection(models.Model):
        name = models.CharField(max_length=25, unique=True)
        code = models.UUIDField(unique=True, default=uuid.uuid4)

    class NamedCollectionView(CRUDView):
        model = NamedCollection
        fields = ["name", "code"]

        lookup_field = "code"
        path_converter = "uuid"
        url_base = "named-collections"

  Will generate URLs such as ``/named-collections/``,
  ``/named-collections/<uuid:code>/``, and so on. URL patterns will be named
  using ``url_base``: "named-collections-list", "named-collections-detail", and
  so on.

  Thanks to Kasun Herath for preliminary discussion and exploration here.

* BREAKING CHANGE. In order to facilitate the above the ``object_list``
  template tag now takes the whole ``view`` from the context, rather than just
  the ``view.fields``.

  If you've overridden the ``object_list.html`` template and are still using
  the ``object_list`` template tag, you will need to update your usage to be
  like this:

  .. code-block: html+django

    {% object_list object_list view %}

* Improved app folder discovery in mktemplate command.

  Thanks to Andrew Miller.

24.3
====

* Added the used ``filterset`` to list-view context.

* Added CI testing for supported Python and Django versions. (Python 3.10
  onwards; Django 4.2 onwards, including the development branch.)

  Thanks to Josh Thomas.

* Added CI build for the documentation.

  Thanks to Eduardo Enriquez

24.2
====

* Added the ``mktemplate`` management command to create an override template from the
  the active default templates for the specified model and CRUD action.

  See ``./manage.py mktemplate --help`` for full details.

24.1
====

* Fixed an incorrect type annotation, that led to incorrect IDE warnings.

23.11
=====

* Adjusted object form template for multipart forms.

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
