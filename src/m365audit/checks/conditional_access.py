"""CA-POLICY: ensure Conditional Access policies exist and are enabled."""
from __future__ import annotations

from ..config import Settings
from ..graph import GraphClient
from ..models import Finding, Severity
from .base import Check


class ConditionalAccessCheck(Check):
    id = "CA-POLICY"
    title = "Conditional Access baseline"

    def run(self, client: GraphClient, settings: Settings) -> list[Finding]:
        policies = list(client.get_all("/identity/conditionalAccess/policies"))
        enabled = [p for p in policies if p.get("state") == "enabled"]

        if not policies:
            return [
                Finding(
                    check_id=self.id,
                    title="No Conditional Access policies",
                    severity=Severity.HIGH,
                    detail="The tenant has no Conditional Access policies; baseline access controls are missing.",
                )
            ]
        if not enabled:
            return [
                Finding(
                    check_id=self.id,
                    title=f"{len(policies)} CA policies but none enabled",
                    severity=Severity.HIGH,
                    detail="All Conditional Access policies are disabled or report-only.",
                    evidence={"total": len(policies)},
                )
            ]
        return []
