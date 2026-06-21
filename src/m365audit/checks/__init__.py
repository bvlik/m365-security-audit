"""Check registry — every Check subclass listed here is run by the CLI."""
from .mfa_registration import MfaRegistrationCheck
from .privileged_roles import PrivilegedRolesCheck

ALL_CHECKS = [
    PrivilegedRolesCheck(),
    MfaRegistrationCheck(),
]
