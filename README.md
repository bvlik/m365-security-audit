<div align="center">

# 🛡️ m365-security-audit

**Read-only security posture auditor for Microsoft 365 / Entra ID.**
Authenticates with a least-privilege app registration, runs a suite of security checks against the Microsoft Graph API, and produces a scored report (console · JSON · HTML).

![Python](https://img.shields.io/badge/Python-3.10+-0A1929?style=for-the-badge&logo=python&logoColor=12ABDB)
![Microsoft Graph](https://img.shields.io/badge/Microsoft_Graph-API-0A1929?style=for-the-badge&logo=microsoft&logoColor=12ABDB)
![Read--only](https://img.shields.io/badge/Mode-Read--only-0070AD?style=for-the-badge)

</div>

---

## Why

In a Microsoft 365 tenant, security drift is silent: global admins pile up, MFA stays unregistered, legacy auth lingers, Conditional Access has gaps. This tool gives a **fast, repeatable, read-only** snapshot of that posture — the kind of baseline review done at the start of a cloud security engagement.

> ⚠️ **Defensive / read-only by design.** Every Graph call is a `GET`. The app registration only requests `*.Read.*` permissions. The tool never modifies the tenant.

## Checks (v0)

| ID | Check | Severity | What it flags |
|----|-------|----------|---------------|
| `PRIV-ROLES` | Privileged role assignments | High | Too many Global Administrators, privileged accounts |
| `MFA-REG` | MFA registration coverage | High | Users (esp. admins) without registered MFA |
| `CA-POLICY` | Conditional Access baseline *(next)* | Medium | Missing/disabled CA policies |
| `LEGACY-AUTH` | Legacy authentication *(next)* | High | Sign-ins using legacy protocols |

## Architecture

```
src/m365audit/
├── cli.py            # entrypoint (argparse)
├── config.py         # env-based settings (TENANT/CLIENT/SECRET)
├── graph.py          # MSAL auth + paginated Graph client
├── models.py         # Severity / Finding / CheckResult
├── report.py         # console (rich) + JSON output
└── checks/
    ├── base.py       # Check abstract base
    ├── privileged_roles.py
    └── mfa_registration.py
```

Adding a check = drop one file in `checks/` subclassing `Check`. The registry auto-collects it.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill TENANT_ID / CLIENT_ID / CLIENT_SECRET
python -m m365audit --format console,json
```

### Required Graph application permissions (admin-consented, read-only)
`Directory.Read.All` · `RoleManagement.Read.Directory` · `Reports.Read.All` · `Policy.Read.All`

## Output

- **Console**: color-coded table by severity (via `rich`)
- **JSON**: machine-readable findings (`report.json`) for pipelines/SIEM ingestion

## Roadmap

- [ ] Conditional Access & legacy-auth checks
- [ ] HTML report (Jinja2) with executive summary
- [ ] CIS Microsoft 365 Benchmark mapping
- [ ] CI mode (exit code on High findings)

## Disclaimer

For use on tenants you are authorized to audit. Read-only, but always run security tooling with permission.
