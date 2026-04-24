#!/usr/bin/env python3
"""
Learner deploy without gse-one: uses .env (COOLIFY_*, DEPLOY_*) and Coolify API v1.

Does not print secrets. Requires public Git repo + root Dockerfile (port 8080).
Set FLASK_SECRET_KEY in Coolify UI (or add to .env — script does not send it unless API supports).
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

from coolify_fetch_logs import post_deploy_logs_optional_wait

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path: Path) -> None:
    if not path.is_file():
        print("No .env file in project root.", file=sys.stderr)
        sys.exit(1)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def require(keys: list[str]) -> None:
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        print(f"Missing in .env: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def sanitize_label(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        print("DEPLOY_USER is empty after sanitizing.", file=sys.stderr)
        sys.exit(1)
    return s[:48]


def api_request(
    base: str,
    token: str,
    method: str,
    path: str,
    body: dict | None = None,
) -> tuple[int, dict | list | None]:
    url = base.rstrip("/") + path
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
            code = resp.status
            if not raw:
                return code, None
            return code, json.loads(raw)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} {path}: {err_body[:800]}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    os.chdir(ROOT)
    load_env(ENV_PATH)
    require(["COOLIFY_URL", "COOLIFY_API_TOKEN", "DEPLOY_DOMAIN", "DEPLOY_USER"])

    base = os.environ["COOLIFY_URL"].rstrip("/")
    token = os.environ["COOLIFY_API_TOKEN"]
    domain = os.environ["DEPLOY_DOMAIN"].strip().lower().rstrip(".")
    deploy_user = sanitize_label(os.environ["DEPLOY_USER"])
    project_name = f"gse-{deploy_user}"
    app_slug = f"sell-tax-free-{deploy_user}"
    fqdn = f"{app_slug}.{domain}"
    # Coolify/Traefik: port in the domain tells Coolify to emit loadbalancer.server.port
    # (fixes "no available server" on custom HTTPS domains). Browser URL stays https://host/ without :8080.
    domain_for_coolify = f"https://{fqdn}:8080"

    git_repo = os.environ.get("DEPLOY_GIT_REPO", "https://github.com/biesdorf-code/sell-tax-free.git")
    git_branch = os.environ.get("DEPLOY_GIT_BRANCH", "main")

    _, servers = api_request(base, token, "GET", "/api/v1/servers")
    if not isinstance(servers, list) or not servers:
        print("No servers in Coolify — ask your instructor.", file=sys.stderr)
        sys.exit(1)
    if len(servers) > 1:
        print(
            "[Inform] Multiple Coolify servers; using the first. Set COOLIFY_SERVER_UUID to override.",
            file=sys.stderr,
        )
    server_uuid = os.environ.get("COOLIFY_SERVER_UUID") or str(servers[0].get("uuid") or "")
    if not server_uuid:
        print("Could not read server uuid.", file=sys.stderr)
        sys.exit(1)

    _, projects = api_request(base, token, "GET", "/api/v1/projects")
    if not isinstance(projects, list):
        print("Unexpected /projects response.", file=sys.stderr)
        sys.exit(1)

    project_uuid = None
    for p in projects:
        if (p.get("name") or "").strip() == project_name:
            project_uuid = p.get("uuid")
            break

    if not project_uuid:
        code, created = api_request(
            base, token, "POST", "/api/v1/projects", {"name": project_name}
        )
        if not isinstance(created, dict) or "uuid" not in created:
            print("Create project failed.", file=sys.stderr)
            sys.exit(1)
        project_uuid = created["uuid"]
        print(f"Created Coolify project: {project_name}")

    _, envs = api_request(base, token, "GET", f"/api/v1/projects/{project_uuid}/environments")
    if not isinstance(envs, list):
        print("Unexpected environments list.", file=sys.stderr)
        sys.exit(1)

    env_name = "production"
    env_uuid = None
    for e in envs:
        if (e.get("name") or "").strip() == env_name:
            env_uuid = e.get("uuid")
            break

    if not env_uuid:
        code, eco = api_request(
            base,
            token,
            "POST",
            f"/api/v1/projects/{project_uuid}/environments",
            {"name": env_name},
        )
        if not isinstance(eco, dict) or "uuid" not in eco:
            print("Create environment failed.", file=sys.stderr)
            sys.exit(1)
        env_uuid = eco["uuid"]
        print(f"Created environment: {env_name}")

    _, apps = api_request(base, token, "GET", "/api/v1/applications")
    if not isinstance(apps, list):
        print("Unexpected applications list.", file=sys.stderr)
        sys.exit(1)

    app_uuid = None
    for a in apps:
        if (a.get("name") or "").strip() == app_slug:
            app_uuid = a.get("uuid")
            break

    if app_uuid:
        print(f"Found existing app {app_slug}; ensuring domain includes :8080 for Traefik, then redeploy…")
        api_request(
            base,
            token,
            "PATCH",
            f"/api/v1/applications/{app_uuid}",
            {"domains": domain_for_coolify, "ports_exposes": "8080"},
        )
        api_request(base, token, "GET", f"/api/v1/deploy?uuid={app_uuid}&force=true")
        print(f"Redeploy started. Open: https://{fqdn}")
        post_deploy_logs_optional_wait(base, token, app_uuid)
        return

    payload = {
        "project_uuid": project_uuid,
        "server_uuid": server_uuid,
        "environment_name": env_name,
        "environment_uuid": env_uuid,
        "git_repository": git_repo,
        "git_branch": git_branch,
        "build_pack": "dockerfile",
        "ports_exposes": "8080",
        "name": app_slug,
        "domains": domain_for_coolify,
        "instant_deploy": True,
        "health_check_enabled": True,
        "health_check_path": "/",
        "health_check_port": "8080",
        "autogenerate_domain": False,
    }

    code, created = api_request(base, token, "POST", "/api/v1/applications/public", payload)
    if code not in (200, 201) or not isinstance(created, dict):
        print("Create application failed.", file=sys.stderr)
        sys.exit(1)
    new_uuid = created.get("uuid")
    print(f"Application created (uuid={new_uuid}). Build/deploy should start in Coolify.")
    print(f"Target URL (after DNS + SSL): https://{fqdn}")
    print(f"(Coolify domain field set to {domain_for_coolify} for correct Traefik routing.)")
    print("Add FLASK_SECRET_KEY under the app in Coolify if sessions should be secure.")
    if new_uuid:
        post_deploy_logs_optional_wait(base, token, str(new_uuid))


if __name__ == "__main__":
    main()
