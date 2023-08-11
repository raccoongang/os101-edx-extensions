from social_core.backends.orcid import ORCIDOAuth2, ORCIDMemberOAuth2Sandbox
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError

from ..models import ExtendedUserProfile

class ORCIDAuthMixin:
    DEFAULT_SCOPE = ['/authenticate', '/read-limited', '/activities/update', '/person/update']

    def get_user_details(self, response):
        """Return user details from ORCID account"""
        orcid_identifier = response.get('orcid-identifier')
        orcid_id = orcid_identifier.get('path') if orcid_identifier else ''
        try:
            ExtendedUserProfile.ORCID_ID_VALIDATOR(orcid_id)
        except ValidationError:
            raise AuthFailedError(_('There was an error receiving your ORCID information. Please check your ORCID account.'))

        fullname = first_name = last_name = email = ''
        person = response.get('person')

        if person:
            name = person.get('name')

            if name:
                first_name = name.get('given-names')
                first_name = first_name.get('value', '') if first_name else ''

                last_name = name.get('family-name')
                last_name = last_name.get('value', '') if last_name else ''

                fullname = first_name
                if last_name:
                    fullname += f' {last_name}'

            emails = person.get('emails')
            if emails:
                emails_list = emails.get('email')
                if emails_list and len(emails_list) > 0:
                    email = emails_list[0].get('email', '')

                    if len(emails_list) > 1:
                        for email_dict in emails_list:
                            if email_dict.get('primary'):
                                email = email_dict['email']
                                break
                    else:
                        email = emails_list[0].get('email', '')

        return {
            'email': email,
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name,
            'orcid_id': orcid_id,
            'username': "",
        }


class ORCIDOAuth2OeX(ORCIDAuthMixin, ORCIDOAuth2):
    pass

class SandboxORCIDAuth2OeX(ORCIDAuthMixin, ORCIDMemberOAuth2Sandbox):
    pass
