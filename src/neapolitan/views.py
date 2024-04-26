import enum

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage, Paginator
from django.forms import models as model_forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import classonlymethod
from django.utils.functional import classproperty
from django.utils.translation import gettext as _
from django.views.generic import View
from django_filters.filterset import filterset_factory


# A CRUDView is a view that can perform all the CRUD operations on a model. The
# `role` attribute determines which operations are available for a given
# as_view() call.
class Role(enum.Enum):
    LIST = "list"
    DETAIL = "detail"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    def handlers(self):
        match self:
            case Role.LIST:
                return {"get": "list"}
            case Role.DETAIL:
                return {"get": "detail"}
            case Role.CREATE:
                return {
                    "get": "show_form",
                    "post": "process_form",
                }
            case Role.UPDATE:
                return {
                    "get": "show_form",
                    "post": "process_form",
                }
            case Role.DELETE:
                return {
                    "get": "confirm_delete",
                    "post": "process_deletion",
                }

    def extra_initkwargs(self):
        # Provide template_name_suffix, "_list", "_detail", "_form", etc. for Role.
        match self:
            case Role.LIST:
                return {"template_name_suffix": "_list"}
            case Role.DETAIL:
                return {"template_name_suffix": "_detail"}
            case Role.CREATE | Role.UPDATE:
                return {"template_name_suffix": "_form"}
            case Role.DELETE:
                return {"template_name_suffix": "_confirm_delete"}

    @property
    def url_name_component(self):
        return self.value

    def url_pattern(self, view_cls):
        url_base = view_cls.url_base
        url_kwarg = view_cls.lookup_url_kwarg or view_cls.lookup_field
        path_converter = view_cls.path_converter
        match self:
            case Role.LIST:
                return f"{url_base}/"
            case Role.DETAIL:
                return f"{url_base}/<{path_converter}:{url_kwarg}>/"
            case Role.CREATE:
                return f"{url_base}/new/"
            case Role.UPDATE:
                return f"{url_base}/<{path_converter}:{url_kwarg}>/edit/"
            case Role.DELETE:
                return f"{url_base}/<{path_converter}:{url_kwarg}>/delete/"

    def get_url(self, view_cls):
        return path(
            self.url_pattern(view_cls),
            view_cls.as_view(role=self),
            name=f"{view_cls.url_base}-{self.url_name_component}"
        )

    def reverse(self, view, object=None):
        url_name = f"{view.url_base}-{self.url_name_component}"
        url_kwarg = view.lookup_url_kwarg or view.lookup_field
        match self:
            case Role.LIST | Role.CREATE:
                return reverse(url_name)
            case _:
                return reverse(
                    url_name,
                    kwargs={url_kwarg: getattr(object, view.lookup_field)},
                )



class CRUDView(View):
    """
    CRUDView is Neapolitan's core. It provides the standard list, detail,
    create, edit, and delete views for a model, as well as the hooks you need to
    be able to customise any part of that.
    """

    role: Role
    model = None
    fields = None  # TODO: handle this being None.

    # Object lookup parameters. These are used in the URL kwargs, and when
    # performing the model instance lookup.
    # Note that if unset then `lookup_url_kwarg` defaults to using the same
    # value as `lookup_field`.
    lookup_field = "pk"
    lookup_url_kwarg = None
    path_converter = "int"
    object = None

    # All the following are optional, and fall back to default values
    # based on the 'model' shortcut.
    # Each of these has a corresponding `.get_<attribute>()` method.
    queryset = None
    form_class = None
    template_name = None
    context_object_name = None

    # Pagination parameters.
    # Set `paginate_by` to an integer value to turn pagination on.
    paginate_by = None
    page_kwarg = "page"
    allow_empty = True

    # Suffix that should be appended to automatically generated template names.
    template_name_suffix = None

    def list(self, request, *args, **kwargs):
        """GET handler for the list view."""

        queryset = self.get_queryset()
        filterset = self.get_filterset(queryset)
        if filterset is not None:
            queryset = filterset.qs

        if not self.allow_empty and not queryset.exists():
            raise Http404

        paginate_by = self.get_paginate_by()
        if paginate_by is None:
            # Unpaginated response
            self.object_list = queryset
            context = self.get_context_data(
                page_obj=None,
                is_paginated=False,
                paginator=None,
                filterset=filterset,
            )
        else:
            # Paginated response
            page = self.paginate_queryset(queryset, paginate_by)
            self.object_list = page.object_list
            context = self.get_context_data(
                page_obj=page,
                is_paginated=page.has_other_pages(),
                paginator=page.paginator,
                filterset=filterset,
            )

        return self.render_to_response(context)

    def detail(self, request, *args, **kwargs):
        """GET handler for the detail view."""

        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)

    def show_form(self, request, *args, **kwargs):
        """GET handler for the create and update form views."""

        if self.role is Role.UPDATE:
            self.object = self.get_object()
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def process_form(self, request, *args, **kwargs):
        """POST handler for the create and update form views."""

        if self.role is Role.UPDATE:
            self.object = self.get_object()
        form = self.get_form(
            data=request.POST,
            files=request.FILES,
            instance=self.object,
        )
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def confirm_delete(self, request, *args, **kwargs):
        """GET handler for the delete confirmation view."""

        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)

    def process_deletion(self, request, *args, **kwargs):
        """POST handler for the delete confirmation view."""

        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    # Queryset and object lookup

    def get_queryset(self):
        """
        Returns the base queryset for the view.

        Either used as a list of objects to display, or as the queryset
        from which to perform the individual object lookup.
        """
        if self.queryset is not None:
            return self.queryset._clone()

        if self.model is not None:
            return self.model._default_manager.all()

        msg = (
            "'%s' must either define 'queryset' or 'model', or override "
            + "'get_queryset()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        try:
            lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        except KeyError:
            msg = "Lookup field '%s' was not provided in view kwargs to '%s'"
            raise ImproperlyConfigured(
                msg % (lookup_url_kwarg, self.__class__.__name__)
            )

        return get_object_or_404(queryset, **lookup)

    # Form handling

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.form_class is not None:
            return self.form_class

        if self.model is not None and self.fields is not None:
            return model_forms.modelform_factory(self.model, fields=self.fields)

        msg = (
            "'%s' must either define 'form_class' or both 'model' and "
            "'fields', or override 'get_form_class()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_form(self, data=None, files=None, **kwargs):
        """
        Returns a form instance.
        """
        cls = self.get_form_class()
        return cls(data=data, files=files, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        assert self.model is not None, (
            "'%s' must define 'model' or override 'get_success_url()'"
            % self.__class__.__name__
        )
        if self.role is Role.DELETE:
            success_url = reverse(f"{self.url_base}-list")
        else:
            success_url = reverse(
                f"{self.url_base}-detail", kwargs={"pk": self.object.pk}
            )
        return success_url

    # Pagination and filtering

    def get_paginate_by(self):
        """
        Returns the size of pages to use with pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, page_size):
        """
        Returns a paginator instance.
        """
        return Paginator(queryset, page_size)

    def paginate_queryset(self, queryset, page_size):
        """
        Paginates a queryset, and returns a page object.
        """
        paginator = self.get_paginator(queryset, page_size)
        page_kwarg = self.kwargs.get(self.page_kwarg)
        page_query_param = self.request.GET.get(self.page_kwarg)
        page_number = page_kwarg or page_query_param or 1
        try:
            page_number = int(page_number)
        except ValueError:
            if page_number == "last":
                page_number = paginator.num_pages
            else:
                msg = "Page is not 'last', nor can it be converted to an int."
                raise Http404(_(msg))

        try:
            return paginator.page(page_number)
        except InvalidPage as exc:
            msg = "Invalid page (%s): %s"
            raise Http404(_(msg) % (page_number, str(exc)))

    def get_filterset(self, queryset=None):
        filterset_class = getattr(self, "filterset_class", None)
        filterset_fields = getattr(self, "filterset_fields", None)

        if filterset_class is None and filterset_fields:
            filterset_class = filterset_factory(self.model, fields=filterset_fields)

        if filterset_class is None:
            return None

        return filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )

    # Response rendering

    def get_context_object_name(self, is_list=False):
        """
        Returns a descriptive name to use in the context in addition to the
        default 'object'/'object_list'.
        """
        if self.context_object_name is not None:
            return self.context_object_name

        elif self.model is not None:
            fmt = "%s_list" if is_list else "%s"
            return fmt % self.model._meta.object_name.lower()

        return None

    def get_context_data(self, **kwargs):
        kwargs["view"] = self
        kwargs["object_verbose_name"] = self.model._meta.verbose_name
        kwargs["object_verbose_name_plural"] = self.model._meta.verbose_name_plural
        kwargs["create_view_url"] = reverse(f"{self.url_base}-create")

        if getattr(self, "object", None) is not None:
            kwargs["object"] = self.object
            context_object_name = self.get_context_object_name()
            if context_object_name:
                kwargs[context_object_name] = self.object

        if getattr(self, "object_list", None) is not None:
            kwargs["object_list"] = self.object_list
            context_object_name = self.get_context_object_name(is_list=True)
            if context_object_name:
                kwargs[context_object_name] = self.object_list

        return kwargs

    def get_template_names(self):
        """
        Returns a list of template names to use when rendering the response.

        If `.template_name` is not specified, uses the
        "{app_label}/{model_name}{template_name_suffix}.html" model template
        pattern, with the fallback to the
        "neapolitan/object{template_name_suffix}.html" default templates.
        """
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            return [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"neapolitan/object{self.template_name_suffix}.html",
            ]
        msg = (
            "'%s' must either define 'template_name' or 'model' and "
            "'template_name_suffix', or override 'get_template_names()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def render_to_response(self, context):
        """
        Given a context dictionary, returns an HTTP response.
        """
        return TemplateResponse(
            request=self.request, template=self.get_template_names(), context=context
        )

    # URLs and view callables

    @classonlymethod
    def as_view(cls, role: Role, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    "The method name %s is not accepted as a keyword argument "
                    "to %s()." % (key, cls.__name__)
                )
            if key in [
                "list",
                "detail",
                "show_form",
                "process_form",
                "confirm_delete",
                "process_deletion",
            ]:
                raise TypeError(
                    "CRUDView handler name %s is not accepted as a keyword argument "
                    "to %s()." % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. as_view "
                    "only accepts arguments that are already "
                    "attributes of the class." % (cls.__name__, key)
                )

        def view(request, *args, **kwargs):
            self = cls(**initkwargs, **role.extra_initkwargs())
            self.role = role
            self.setup(request, *args, **kwargs)
            if not hasattr(self, "request"):
                raise AttributeError(
                    f"{cls.__name__} instance has no 'request' attribute. Did you "
                    "override setup() and forget to call super()?"
                )

            for method, action in role.handlers().items():
                handler = getattr(self, action)
                setattr(self, method, handler)

            return self.dispatch(request, *args, **kwargs)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        # Mark the callback if the view class is async.
        # if cls.view_is_async:
        #     markcoroutinefunction(view)

        return view

    @classproperty
    def url_base(cls):
        """
        The base component of generated URLs.

        Defaults to the model's name, but may be overridden by setting
        `url_base` directly on the class, overriding this property::

            class AlternateCRUDView(CRUDView):
                model = Bookmark
                url_base = "something-else"
        """
        return cls.model._meta.model_name

    @classonlymethod
    def get_urls(cls, roles=None):
        """Classmethod to generate URL patterns for the view."""
        if roles is None:
            roles = iter(Role)
        return [role.get_url(cls) for role in roles]
