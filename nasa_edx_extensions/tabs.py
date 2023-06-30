from lms.djangoapps.courseware.tabs import DatesTab
from lms.djangoapps.discussion.plugins import DiscussionTab
from django.utils.translation import ugettext as _


class DatesTabUnabled(DatesTab):
    @classmethod
    def is_enabled(cls, course, user=None):  # pylint: disable=unused-argument
        return False


class DiscussionTabRedirect(DiscussionTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = _("Community")
        self.title = _("Community")

    @property
    def link_func(self):
        # TODO: transform hardcoded link to site config/settings variable with default value
        return lambda course, reverse_func: "https://github.com/nasa/Transform-to-Open-Science/discussions"
