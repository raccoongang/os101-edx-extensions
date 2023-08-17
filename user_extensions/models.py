from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

User = get_user_model()


class ExtendedUserProfile(models.Model):
    """Extend user with additional data."""

    ORCID_ID_VALIDATOR = RegexValidator(
        r'^\d{4}-\d{4}-\d{4}-\d{3}([0-9X])$|^none$',
        message=_("ORCID ID must be in the format: '0000-0000-0000-0000' (last number can be 'X') or 'none'")
    )

    SCIENCE_COMMUNITY_CHOICES = [
        ('astrophysics', _('Astrophysics')),
        ('bio_physical_sciences', _('Biological and Physical Sciences')),
        ('earth_science', _('Earth Science')),
        ('heliophysics', _('Heliophysics')),
        ('planetary_science', _('Planetary Science')),
        ('other', _('Other')),
    ]

    CAREER_STAGE_CHOICES = [
        ('college_student', _('College student')),
        ('graduate_student', _('Graduate student')),
        ('less_than_5_years', _('<5 years highest degree')),
        ('5_to_10_years', _('5-10 years highest degree')),
        ('more_than_10_years', _('10+ years highest degree')),
    ]

    EXTENDED_GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('non_binary', _('Non-Binary')),
        ('prefer_not_to_say', _('Prefer not to say / My option is not listed')),
    ]

    RACE_ETHNICITY_CHOICES = [
        ('american_indian', _('American Indian or Alaskan Native')),
        ('asian', 'Asian'),
        ('black', _('Black or African American')),
        ('hispanic_latino', _('Hispanic or Latino')),
        ('white', _('White')),
        ('prefer_not_to_say', _('Prefer not to say / My option is not listed')),
    ]

    user = models.OneToOneField(User, unique=True, related_name='extended_user_profile', on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, blank=True, default='')
    orcid_id = models.CharField(max_length=20, default="none", validators=[ORCID_ID_VALIDATOR])
    subscribe_to_emails = models.BooleanField(default=False)
    science_community = models.CharField(max_length=255, choices=SCIENCE_COMMUNITY_CHOICES, null=True, blank=False, default="other")
    career_stage = models.CharField(max_length=255, choices=CAREER_STAGE_CHOICES, null=True, blank=False, default="college_student")
    extended_gender = models.CharField(max_length=255, choices=EXTENDED_GENDER_CHOICES, null=True, blank=False, default="prefer_not_to_say")
    race_ethnicity = models.CharField(max_length=255, choices=RACE_ETHNICITY_CHOICES, null=True, blank=False, default="prefer_not_to_say")

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        qs = ExtendedUserProfile.objects.exclude(
            orcid_id="none"
        ).filter(orcid_id=self.orcid_id)
        if qs.exists():
            raise ValidationError({'orcid_id':['orcid_id must be unique per site',]})
