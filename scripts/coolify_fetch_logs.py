#!/usr/bin/env python3
"""Fetch last deployment (build) logs + app status from Coolify (uses .env).

Runtime container logs require a running container; Coolify returns HTTP 400
``Application is not running`` otherwise — build output is still in the deployment record.
"""

from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path: Path) -> None:
    if not path.is_file():
        print("No .env in project root.", file=sys.stderr)
        sys.exit(1)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def sanitize_label(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:48] if s else ""


def api_json(base: str, token: str, method: str, path_qs: str) -> tuple[int, object | None]:
    url = base.rstrip("/") + path_qs
    req = urllib.request.Request(
        url,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        raw = resp.read().decode("utf-8")
        code = resp.status
        if not raw:
            return code, None
        return code, json.loads(raw)


def normalize_deployment_list(body: object) -> list:
    if isinstance(body, list):
        return body
    if isinstance(body, dict):
        for key in ("data", "deployments", "items", "result"):
            v = body.get(key)
            if isinstance(v, list):
                return v
    return []


def deployment_record_uuid(d: dict) -> str | None:
    for key in ("deployment_uuid", "uuid", "id"):
        v = d.get(key)
        if v and isinstance(v, str):
            return v
    return None


def main() -> None:
    os.chdir(ROOT)
    load_env(ENV_PATH)
    for k in ("COOLIFY_URL", "COOLIFY_API_TOKEN", "DEPLOY_USER"):
        if not os.environ.get(k):
            print(f"Missing {k} in .env", file=sys.stderr)
            sys.exit(1)

    base = os.environ["COOLIFY_URL"].rstrip("/")
    token = os.environ["COOLIFY_API_TOKEN"]
    app_slug = f"sell-tax-free-{sanitize_label(os.environ['DEPLOY_USER'])}"
    lines = int(os.environ.get("COOLIFY_LOG_LINES", "400"))

    try:
        _, apps = api_json(base, token, "GET", "/api/v1/applications")
    except urllib.error.HTTPError as e:
        print(f"List applications failed: HTTP {e.code}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(apps, list):
        print("Unexpected applications response", file=sys.stderr)
        sys.exit(1)

    app_uuid = None
    for a in apps:
        if (a.get("name") or "").strip() == app_slug:
            app_uuid = a.get("uuid")
            break

    if not app_uuid:
        print(f"No application named {app_slug!r}. Available names:", file=sys.stderr)
        for a in apps[:30]:
            print(f"  - {a.get('name')}", file=sys.stderr)
        sys.exit(1)

    print(f"=== Application: {app_slug} (uuid={app_uuid}) ===\n")

    try:
        _, app_one = api_json(base, token, "GET", f"/api/v1/applications/{app_uuid}")
    except urllib.error.HTTPError:
        app_one = None

    if isinstance(app_one, dict):
        snap = {
            k: app_one.get(k)
            for k in (
                "status",
                "fqdn",
                "ports_exposes",
                "git_branch",
                "git_commit_sha",
                "build_pack",
                "health_check_enabled",
                "health_check_port",
            )
            if app_one.get(k) is not None
        }
        print("--- Current application (summary) ---")
        print(json.dumps(snap, indent=2))
        print()

    depls: list = []
    try:
        _, raw_depls = api_json(
            base,
            token,
            "GET",
            f"/api/v1/deployments/applications/{app_uuid}?take=5&skip=0",
        )
        depls = normalize_deployment_list(raw_depls)
    except urllib.error.HTTPError as e:
        print(f"List deployments: HTTP {e.code} (continuing)\n", file=sys.stderr)

    dep_uuid: str | None = None
    if depls:
        print("--- Recent deployments (raw summary) ---")
        for i, d in enumerate(depls[:5]):
            if isinstance(d, dict):
                dep_uuid = deployment_record_uuid(d) or dep_uuid
                slim = {k: d.get(k) for k in d if k in (
                    "deployment_uuid", "uuid", "status", "commit", "commit_message",
                    "created_at", "updated_at", "application_name", "logs",
                )}
                if slim.get("logs") and isinstance(slim["logs"], str) and len(slim["logs"]) > 200:
                    slim["logs"] = slim["logs"][:200] + "… (truncated; see deployment fetch below)"
                print(json.dumps(slim, indent=2, default=str))
                if i < len(depls) - 1:
                    print()
        print()

    # Prefer explicit latest deployment fetch (includes full logs field)
    first = depls[0] if depls and isinstance(depls[0], dict) else {}
    latest_uuid = deployment_record_uuid(first)
    if latest_uuid:
        try:
            _, dep_one = api_json(base, token, "GET", f"/api/v1/deployments/{latest_uuid}")
        except urllib.error.HTTPError as e:
            dep_one = None
            print(f"GET deployment {latest_uuid}: HTTP {e.code}\n", file=sys.stderr)
        if isinstance(dep_one, dict) and dep_one.get("logs"):
            print("--- Last deployment: build / deploy logs ---")
            print(dep_one["logs"])
            print()
        elif isinstance(dep_one, dict):
            print("--- Last deployment (no logs field in response) ---")
            print(json.dumps({k: dep_one.get(k) for k in dep_one if k != "logs"}, indent=2, default=str))
            print()

    # Runtime logs only when container is up
    try:
        _, log_body = api_json(
            base,
            token,
            "GET",
            f"/api/v1/applications/{app_uuid}/logs?lines={lines}",
        )
        print(f"--- Runtime logs (last {lines} lines) ---")
        if isinstance(log_body, dict) and "logs" in log_body:
            print(log_body["logs"])
        else:
            print(json.dumps(log_body, indent=2) if log_body else "(empty)")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:2000]
        print("--- Runtime logs ---")
        print(f"Not available: HTTP {e.code} — {err}")
        print(
            "\nThis usually means the application container is not running. "
            "Use the deployment logs above (build phase) to see Docker/build errors."
        )


if __name__ == "__main__":
    main()
