import logging
from social_core.backends.orcid import ORCIDOAuth2, ORCIDMemberOAuth2Sandbox
from django.core.exceptions import ValidationError
from crum import get_current_request

from ..models import ExtendedUserProfile


log = logging.getLogger(__name__)

class ORCIDAuthMixin:
    DEFAULT_SCOPE = ['/authenticate', '/read-limited', '/activities/update', '/person/update']

    def get_user_details(self, response):
        """Return user details from ORCID account"""
        orcid_identifier = response.get('orcid-identifier')
        orcid_id = orcid_identifier.get('path') if orcid_identifier else ''
        try:
            ExtendedUserProfile.ORCID_ID_VALIDATOR(orcid_id)
        except ValidationError:
            log.exception(f"There was an error receiving user ORCID information. Invalid orcid_id: {orcid_id}\nResponse: {response}")
            orcid_id = "none"

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

        request = get_current_request()
        email_to_update_orcid = ''
        if request.user.is_anonymous:
            email_to_update_orcid = email
        else:
            email_to_update_orcid = request.user.email

        ExtendedUserProfile.objects.filter(user__email=email_to_update_orcid).update(orcid_id=orcid_id)

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
