from django import forms
from .models import ExtendedUserProfile
from django.conf import settings
from django.utils.translation import gettext as _


class ExtendedUserProfileForm(forms.ModelForm):
    """
    Form that is used to extend registration form with additional
    fields taken from ExtendedUserProfile model
    """
    SUBSCRIBE_TO_EMAILS_CHOICES = [(0, _('No')), (1, _('Yes'))]

    subscribe_to_emails = forms.ChoiceField(
        label=_("Follow TOPS activities and subscribe to email list?"),
        choices=SUBSCRIBE_TO_EMAILS_CHOICES,
        help_text=_("Please choose whether you would like to subscribe to our email list.")
    )

    class Meta:
        model = ExtendedUserProfile
        fields = (
            'orcid_id',
            'subscribe_to_emails',
            'science_community',
            'career_stage',
            'extended_gender',
            'race_ethnicity',
        )
        labels = {
            'orcid_id': _('ORCID ID'),
            'science_community': _('Scientific community'),
            'career_stage': _('Career stage'),
            'extended_gender': _('Gender'),
            'race_ethnicity': _('Race / Ethnicity')
        }
        help_texts = {
            'orcid_id': _('If you do not have an ORCID ID, put <strong>"none"</strong>. ORCID ID must be in the format: "0000-0000-0000-0000"'),
            'science_community': _('Please choose the scientific community with which you most identify.'),
            'career_stage': _('Please indicate which career stage you most identify with.'),
            'extended_gender': _('Please indicate your gender.'),
            'race_ethnicity': _('Please indicate your race/ethnicity.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in settings.NASA_EXTENDED_PROFILE_FIELDS:
            self.fields[field_name].required = True
