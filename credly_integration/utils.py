import csv
from io import StringIO

from lms.djangoapps.certificates.models import GeneratedCertificate
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from user_extensions.models import ExtendedUserProfile

from .models import CredlyCourseData


def generate_credly_data_csv():
    headers = (
        'Badge Template ID',
        'Recipient Email',
        'Issued To First Name',
        'Issued To Middle Name',
        'Issued To Last Name',
        'Issued at',
        'Expires at',
        'Issuer Earner ID',
        'Group Tag',
        'Country',
        'State or Province',
        'Evidence Name',
        'Evidence URL',
        'URL Evidence Description',
        'Text Evidence Title',
        'Text Evidence Description',
        'Id Evidence Title',
        'Id Evidence Description'
    )

    credly_courses = CourseOverview.objects.exclude(
        credly_course_data__badge_id__isnull=True
    ).exclude(
        credly_course_data__badge_id__exact=''
    ).values_list('id', flat=True)
    certificate_data = GeneratedCertificate.objects.filter(course_id__in=credly_courses)
    output_csv = StringIO()
    csvwriter = csv.writer(output_csv, delimiter=',')
    csvwriter.writerow(headers)
    for cert in certificate_data:
        extended_user_profile = ExtendedUserProfile.objects.filter(user=cert.user).first()
        csvwriter.writerow([
            CredlyCourseData.objects.get(course=cert.course_id).badge_id,
            cert.user.email,
            cert.user.first_name,
            extended_user_profile.middle_name if extended_user_profile else "",
            cert.user.last_name,
            cert.modified_date.strftime("%m/%d/%Y"),
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ])

    return output_csv.getvalue().encode('UTF-8')
