"""Check registry — every Check listed here is run by the CLI."""
from .conditional_access import ConditionalAccessCheck
from .guest_users import GuestUsersCheck
from .mfa_registration import MfaRegistrationCheck
from .privileged_roles import PrivilegedRolesCheck

ALL_CHECKS = [
    PrivilegedRolesCheck(),
    MfaRegistrationCheck(),
    ConditionalAccessCheck(),
    GuestUsersCheck(),
]
