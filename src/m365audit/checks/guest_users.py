"""GUEST-USERS: surface external guest accounts for review."""
from __future__ import annotations

from ..config import Settings
from ..graph import GraphClient
from ..models import Finding, Severity
from .base import Check


class GuestUsersCheck(Check):
    id = "GUEST-USERS"
    title = "Guest account exposure"

    def run(self, client: GraphClient, settings: Settings) -> list[Finding]:
        guests = [
            u.get("userPrincipalName", u.get("id"))
            for u in client.get_all(
                "/users",
                {"$filter": "userType eq 'Guest'", "$select": "userPrincipalName,userType"},
            )
        ]
        if not guests:
            return []
        return [
            Finding(
                check_id=self.id,
                title=f"{len(guests)} guest account(s) present",
                severity=Severity.MEDIUM,
                detail="Review external guest accounts for least privilege and staleness.",
                evidence={"sample": guests[:25], "total": len(guests)},
            )
        ]
