from .utils import split_full_name
from .models import ExtendedUserProfile


def do_create_account(base_fn, *args, **kwargs):
    """
    Override function do_create_account for adding in User object
    fields 'first_name', 'last_name' and 'middle_name'.

    Returns a tuple (User, UserProfile, Registration).
    """
    user, profile, registration = base_fn(*args, **kwargs)

    first_name, middle_name, last_name = split_full_name(profile.name)

    ExtendedUserProfile.objects.update_or_create(user=user, middle_name=middle_name)

    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return user, profile, registration
