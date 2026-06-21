"""Environment-based configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    tenant_id: str
    client_id: str
    client_secret: str
    max_global_admins: int = 4

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        missing = [k for k in ("TENANT_ID", "CLIENT_ID", "CLIENT_SECRET") if not os.getenv(k)]
        if missing:
            raise SystemExit(f"Missing required env vars: {', '.join(missing)} (see .env.example)")
        return cls(
            tenant_id=os.environ["TENANT_ID"],
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            max_global_admins=int(os.getenv("MAX_GLOBAL_ADMINS", "4")),
        )
