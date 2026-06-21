"""MFA-REG: flag users without registered MFA, prioritising admins."""
from __future__ import annotations

from ..config import Settings
from ..graph import GraphClient
from ..models import Finding, Severity
from .base import Check


class MfaRegistrationCheck(Check):
    id = "MFA-REG"
    title = "MFA registration coverage"

    def run(self, client: GraphClient, settings: Settings) -> list[Finding]:
        findings: list[Finding] = []
        no_mfa_users: list[str] = []
        no_mfa_admins: list[str] = []

        # Reports.Read.All — registration details per user.
        for u in client.get_all("/reports/authenticationMethods/userRegistrationDetails"):
            if u.get("isMfaRegistered"):
                continue
            upn = u.get("userPrincipalName", u.get("id", "unknown"))
            if u.get("isAdmin"):
                no_mfa_admins.append(upn)
            else:
                no_mfa_users.append(upn)

        if no_mfa_admins:
            findings.append(
                Finding(
                    check_id=self.id,
                    title=f"{len(no_mfa_admins)} admin(s) without MFA",
                    severity=Severity.CRITICAL,
                    detail="Privileged accounts without registered MFA are a top compromise vector.",
                    evidence={"admins": no_mfa_admins},
                )
            )
        if no_mfa_users:
            findings.append(
                Finding(
                    check_id=self.id,
                    title=f"{len(no_mfa_users)} user(s) without MFA",
                    severity=Severity.HIGH,
                    detail="Users without registered MFA weaken the tenant's baseline.",
                    evidence={"sample": no_mfa_users[:25], "total": len(no_mfa_users)},
                )
            )
        return findings
