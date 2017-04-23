from django.utils import timezone


def ensure_aware(dt):
    """
    core.utils.ensure_aware
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Will convert datetime.datetime instance from naive into aware,
    or return if instance is already aware.
    """
    if timezone.is_aware(dt):
        return dt

    return timezone.make_aware(dt)
