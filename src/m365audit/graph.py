"""Microsoft Graph client: MSAL client-credentials auth + paginated GET."""
from __future__ import annotations

from typing import Any, Iterator

import msal
import requests

from .config import Settings

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
_SCOPE = ["https://graph.microsoft.com/.default"]


class GraphError(RuntimeError):
    pass


class GraphClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._app = msal.ConfidentialClientApplication(
            client_id=settings.client_id,
            client_credential=settings.client_secret,
            authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        )
        self._session = requests.Session()
        self._token: str | None = None

    def _acquire_token(self) -> str:
        if self._token:
            return self._token
        result = self._app.acquire_token_for_client(scopes=_SCOPE)
        if "access_token" not in result:
            raise GraphError(
                f"Auth failed: {result.get('error')} - {result.get('error_description')}"
            )
        self._token = result["access_token"]
        return self._token

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = path if path.startswith("http") else f"{GRAPH_BASE}{path}"
        resp = self._session.get(
            url,
            headers={"Authorization": f"Bearer {self._acquire_token()}"},
            params=params,
            timeout=30,
        )
        if resp.status_code == 403:
            raise GraphError(f"Forbidden on {path} — check app permissions / admin consent")
        resp.raise_for_status()
        return resp.json()

    def get_all(self, path: str, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Yield every item across @odata.nextLink pages."""
        page = self.get(path, params)
        while True:
            yield from page.get("value", [])
            next_link = page.get("@odata.nextLink")
            if not next_link:
                return
            page = self.get(next_link)
