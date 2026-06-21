"""PRIV-ROLES: enumerate privileged directory roles and their members."""
from __future__ import annotations

from ..config import Settings
from ..graph import GraphClient
from ..models import Finding, Severity
from .base import Check

# Directory roles considered highly privileged (by template display name).
PRIVILEGED_ROLES = {
    "Global Administrator",
    "Privileged Role Administrator",
    "Security Administrator",
    "Exchange Administrator",
    "SharePoint Administrator",
    "User Administrator",
}


class PrivilegedRolesCheck(Check):
    id = "PRIV-ROLES"
    title = "Privileged role assignments"

    def run(self, client: GraphClient, settings: Settings) -> list[Finding]:
        findings: list[Finding] = []
        global_admins: list[str] = []

        for role in client.get_all("/directoryRoles"):
            name = role.get("displayName", "")
            if name not in PRIVILEGED_ROLES:
                continue
            members = [
                m.get("userPrincipalName") or m.get("displayName") or m.get("id")
                for m in client.get_all(f"/directoryRoles/{role['id']}/members")
            ]
            if name == "Global Administrator":
                global_admins = members

            if members:
                findings.append(
                    Finding(
                        check_id=self.id,
                        title=f"{name}: {len(members)} member(s)",
                        severity=Severity.INFO,
                        detail=f"Members holding '{name}'.",
                        evidence={"role": name, "members": members},
                    )
                )

        if len(global_admins) > settings.max_global_admins:
            findings.append(
                Finding(
                    check_id=self.id,
                    title=f"Too many Global Administrators ({len(global_admins)})",
                    severity=Severity.HIGH,
                    detail=(
                        f"{len(global_admins)} Global Admins exceeds the recommended max of "
                        f"{settings.max_global_admins}. Microsoft recommends keeping this small "
                        "and using PIM/just-in-time elevation."
                    ),
                    evidence={"global_admins": global_admins},
                )
            )
        return findings
