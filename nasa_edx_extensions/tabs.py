from lms.djangoapps.courseware.tabs import DatesTab
from lms.djangoapps.discussion.plugins import DiscussionTab


class DatesTabUnabled(DatesTab):
    @classmethod
    def is_enabled(cls, course, user=None):  # pylint: disable=unused-argument
        return False


class DiscussionTabRedirect(DiscussionTab):
    @property
    def link_func(self):
        # TODO: transform hardcoded link to site config/settings variable with default value
        return lambda course, reverse_func: "https://github.com/nasa/Transform-to-Open-Science"
