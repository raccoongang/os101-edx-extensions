Change Log
==========

..
   All enhancements and patches to nasa_edx_extensions will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.
Unreleased
----------

[v1.5.4] - 2023-08-10
~~~~~~~~~~~~~~~~~~~~~
* Override ORCID social core backend to correctly provide user information.
* Extend scopes for ORCID SSO.
* Add sandbox ORCID SSO.
* Override function for getting third party auth context.

[v1.4.4] - 2023-07-21
~~~~~~~~~~~~~~~~~~~~~
* Correct the report link.

[v1.4.3] - 2023-07-09
~~~~~~~~~~~~~~~~~~~~~
* Fix initialization for cms.

[v1.4.2] - 2023-07-09
~~~~~~~~~~~~~~~~~~~~~
* Turn off user_extensions app for cms.

[v1.4.1] - 2023-07-09
~~~~~~~~~~~~~~~~~~~~~
* Introduce feature flag `ENABLE_CREDLY_INTEGRATION` to turn on credly integration feature.

[v1.4.0] - 2023-07-08
~~~~~~~~~~~~~~~~~~~~~
* Extend model `ExtendedUserProfile` to store other extended fields from register page.
* Override `authn_field_can_be_saved` and `modify_error_message_for_fields`.
* Create `ExtendedUserProfileForm` form to pass new fields to frontend-app-authn.
* Extend settings with new registration fields.

[v1.3.0] - 2023-07-03
~~~~~~~~~~~~~~~~~~~~~
* Add `generate_credly_data_csv`` for generate csv report.
* Override `do_create_account`` for adding
  fields `first_name`, `middle_name` and `last_name`.
* Create `user_extensions`` app for extending user functionality.
* Create new model `ExtendedUserProfile` to store `middle_name`.

[v1.2.0] - 2023-06-30
~~~~~~~~~~~~~~~~~~~~~
* Rename discussion tab to `Community`

[v1.1.0] - 2023-06-26
~~~~~~~~~~~~~~~~~~~~~
* Add new model CredlyCourseData for store user`s Badge ID.
* Override advanced_settings_handler view
  where the logic for getting and updating the Credly Badge Template ID field
  has been changed.

[1.0.0] - 2023-06-23
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Turn off `DatesTab`.
* Override `DiscussionTab` for the redirect to external link.
