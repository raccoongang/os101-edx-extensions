from django.db import models
from django.utils.translation import ugettext as _


class CredlyCourseData(models.Model):
    """Store user`s Badge ID for each course."""
    course = models.OneToOneField('course_overviews.CourseOverview', related_name='credly_course_data', on_delete=models.CASCADE)
    badge_id = models.CharField(default='', max_length=100)
