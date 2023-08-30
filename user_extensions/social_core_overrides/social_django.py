from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from social_core.actions import do_disconnect
from social_django.utils import psa

from .utils import unlink_orcid_from_extended_profile

@never_cache
@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    response = do_disconnect(request.backend, request.user, association_id, redirect_name=REDIRECT_FIELD_NAME)
    if backend in ['orcid', 'orcid-sandbox']:
        unlink_orcid_from_extended_profile(request.user)
    return response
