from django.utils.translation import gettext_lazy as _

from common import variables

USER_STATE = (
    (variables.PENDING, _("Pending")),
    (variables.PHONE_VERIFIED, _("Phone number Verified")),
    (variables.USER_VERIFIED, _("User Verified")),
    (variables.DELETED, _("Deleted")),
)
