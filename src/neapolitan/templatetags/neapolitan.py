from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


def action_links(object):
    model_name = object._meta.model_name
    edit_url = reverse(f"{model_name}-update", kwargs={"pk": object.pk})
    delete_url = reverse(f"{model_name}-delete", kwargs={"pk": object.pk})
    links = f"""<a href="{edit_url}">Edit</a> | <a href="{delete_url}">Delete</a>"""
    return mark_safe(links)


@register.inclusion_tag("neapolitan/partial/detail.html")
def object_detail(object, fields):
    def iter():
        for f in fields:
            mf = object._meta.get_field(f)
            yield (mf.verbose_name, mf.value_to_string(object))

    return {"object": iter()}


@register.inclusion_tag("neapolitan/partial/list.html")
def object_list(objects, fields):
    headers = [objects[0]._meta.get_field(f).verbose_name for f in fields]
    object_list = [
        {
            "object": object,
            "fields": [
                object._meta.get_field(f).value_to_string(object) for f in fields
            ],
            "actions": action_links(object),
        }
        for object in objects
    ]
    return {
        "headers": headers,
        "object_list": object_list,
    }
