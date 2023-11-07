from urllib.parse import urljoin

from django.conf import settings
from django.db import models


class CertificateExtraData(models.Model):
    badge_name_override = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="certificate_extra_images", null=True, blank=True)
    course = models.ForeignKey('course_overviews.courseoverview', null=True, on_delete=models.CASCADE)

    @property
    def full_image_url(self):
        if self.image:
            return urljoin(settings.LMS_ROOT_URL, getattr(self.image, 'url', None))
        return None
