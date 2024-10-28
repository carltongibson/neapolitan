from django import template
from django.utils.safestring import mark_safe

from neapolitan.views import Role

register = template.Library()


def action_links(view, object):
    actions = [
        (url, name)
        for url, name in [
            (Role.DETAIL.maybe_reverse(view, object), "View"),
            (Role.UPDATE.maybe_reverse(view, object), "Edit"),
            (Role.DELETE.maybe_reverse(view, object), "Delete"),
        ] if url is not None
    ]
    links = [f"<a href='{url}'>{anchor_text}</a>" for url, anchor_text in actions]
    return mark_safe(" | ".join(links))


@register.inclusion_tag("neapolitan/partial/detail.html")
def object_detail(object, fields):
    """
    Renders a detail view of an object with the given fields.

    Inclusion tag usage::

        {% object_detail object fields %}

    Template: ``neapolitan/partial/detail.html`` - Will render a table of the
    object's fields.
    """

    def iter():
        for f in fields:
            mf = object._meta.get_field(f)
            yield (mf.verbose_name, str(getattr(object, f)))

    return {"object": iter()}


@register.inclusion_tag("neapolitan/partial/list.html")
def object_list(objects, view):
    """
    Renders a list of objects with the given fields.

    Inclusion tag usage::

        {% object_list objects view %}

    Template: ``neapolitan/partial/list.html`` — Will render a table of objects
    with links to view, edit, and delete views.
    """

    fields = view.fields
    headers = [objects[0]._meta.get_field(f).verbose_name for f in fields]
    object_list = [
        {
            "object": object,
            "fields": [{"name": f, "value": str(getattr(object, f))} for f in fields],
            "actions": action_links(view, object),
        }
        for object in objects
    ]
    return {
        "headers": headers,
        "object_list": object_list,
    }
