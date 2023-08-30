from ..models import ExtendedUserProfile

def unlink_orcid_from_extended_profile(user):
    """
    Set orcid_id to none.
    """
    ExtendedUserProfile.objects.filter(user=user).update(orcid_id="none")
