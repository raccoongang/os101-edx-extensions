import pytest
from django.core.exceptions import ValidationError

from user_extensions.models import ExtendedUserProfile

@pytest.mark.parametrize("orcid_id, valid", [
    ("0000-0000-0000-0000", True),
    ("0000-0000-0000-000X", True),
    ("1234-5678-9012-3456", True),
    ("none", True),
    ("0000-0000-0000-00X0", False),
    ("abcd-efgh-ijkl-mnop", False),
    ("123-123-123-123", False),
    ("1234-1234-1234-123", False),
    ("", False),
])
def test_orcid_id_validator(orcid_id, valid):
    validator = ExtendedUserProfile.ORCID_ID_VALIDATOR
    if valid:
        validator(orcid_id)
    else:
        with pytest.raises(ValidationError):
            validator(orcid_id)
