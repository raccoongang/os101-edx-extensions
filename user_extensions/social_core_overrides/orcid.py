from social_core.backends.orcid import ORCIDOAuth2, ORCIDMemberOAuth2Sandbox


class ORCIDAuthMixin:
    DEFAULT_SCOPE = ['/authenticate', '/read-limited', '/activities/update', '/person/update']

    def get_user_details(self, response):
        """Return user details from ORCID account"""
        orcid_identifier = response.get('orcid-identifier')
        fullname = first_name = last_name = email = ''
        person = response.get('person')

        if person:
            name = person.get('name')

            if name:
                first_name = name.get('given-names', {}).get('value', '')
                last_name = name.get('family-name', {}).get('value', '')
                fullname = f"{first_name} {last_name}"

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
            'orcid_id': orcid_identifier['path'],
            'username': "",
        }


class ORCIDOAuth2OeX(ORCIDAuthMixin, ORCIDOAuth2):
    pass

class SandboxORCIDAuth2OeX(ORCIDAuthMixin, ORCIDMemberOAuth2Sandbox):
    pass
