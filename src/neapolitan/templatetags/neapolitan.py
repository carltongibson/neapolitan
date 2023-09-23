from django import template
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


def action_links(object, lookup_field):
    model_name = object._meta.model_name
    try:
        lookup_value = getattr(object, lookup_field)
    except AttributeError:
        raise ImproperlyConfigured(f"Lookup field {lookup_field} doesn't exist on object")

    actions = [
        (reverse(f"{model_name}-detail", kwargs={lookup_field: lookup_value}), "View"),
        (reverse(f"{model_name}-update", kwargs={lookup_field: lookup_value}), "Edit"),
        (reverse(f"{model_name}-delete", kwargs={lookup_field: lookup_value}), "Delete"),
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
            yield (mf.verbose_name, mf.value_to_string(object))

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

    headers = [objects[0]._meta.get_field(f).verbose_name for f in view.fields]
    object_list = [
        {
            "object": object,
            "fields": [
                object._meta.get_field(f).value_to_string(object) for f in view.fields
            ],
            "actions": action_links(object, view.lookup_field),
        }
        for object in objects
    ]
    return {
        "headers": headers,
        "object_list": object_list,
    }
