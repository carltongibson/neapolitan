from django.conf import settings


def get_settings():
    """
    Returns neapolitan settings defined in settings file.
    
    If not defined returns an empty dict.
    """
    try:
        neapolitan_settings = settings.NEAPOLITAN
    except AttributeError:
        return {}
    else:
        return neapolitan_settings
