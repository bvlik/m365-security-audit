"""Abstract base for all checks."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..config import Settings
from ..graph import GraphClient
from ..models import Finding


class Check(ABC):
    #: stable identifier, e.g. "PRIV-ROLES"
    id: str
    #: human-readable title
    title: str

    @abstractmethod
    def run(self, client: GraphClient, settings: Settings) -> list[Finding]:
        """Execute the check and return findings (empty list = pass)."""
        raise NotImplementedError
