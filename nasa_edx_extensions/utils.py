from openedx.core.djangoapps.plugins.constants import ProjectType


def get_project_type(settings):
    """
    Get project type based on `ROOT_URLCONF`.
    """
    if settings.ROOT_URLCONF == 'lms.urls':
        project_type = ProjectType.LMS
    elif settings.ROOT_URLCONF == 'cms.urls':
        project_type = ProjectType.CMS
    else:
        project_type = None

    return project_type
