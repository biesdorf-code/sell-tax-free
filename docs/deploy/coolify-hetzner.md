# Deploy Sell Tax Free — Coolify on Hetzner

Operational companion to the in-app **Deploy to production?** gate (`/deploy`).

## Troubleshooting: “no available server” (Traefik)

If the browser shows a black page with **`no available server`** (and broken HTTPS), Coolify often did not set Traefik’s **`loadbalancer.server.port`** for your app.

**Fix (Coolify UI):** open the application → **Domains** → set the URL to **`https://<your-host>:8080`** (include **`:8080`** even though users open `https://<your-host>/` without the port). Save and **Redeploy**. See [Coolify: No Available Server](https://coolify.io/docs/troubleshoot/applications/no-available-server).

The **`scripts/learner_coolify_deploy.py`** helper sets this domain form automatically on create and on redeploy.

## Learner mode (shared Coolify, no `gse-one` CLI)

If you only have `.env` with `COOLIFY_URL`, `COOLIFY_API_TOKEN`, `DEPLOY_DOMAIN`, and `DEPLOY_USER` (from your instructor), run from the repo root:

```bash
python scripts/learner_coolify_deploy.py
```

This uses the Coolify API to ensure project `gse-<DEPLOY_USER>`, environment `production`, and app `sell-tax-free-<DEPLOY_USER>`, then starts a Dockerfile build from `main`. Add **`FLASK_SECRET_KEY`** in the Coolify UI for that app before relying on sessions in production.

**Post-deploy logs (automatic):** after a deploy is triggered, the script waits for the latest deployment to reach a **finished** or **failed** state (or times out), then prints **build/deploy logs** from Coolify and **runtime logs** from the app container when the platform exposes them. That gives you application-layer output (Gunicorn/Flask stderr, etc.) as soon as the container is up.

| `.env` variable | Default | Meaning |
|-----------------|--------|---------|
| `COOLIFY_FETCH_LOGS_AFTER_DEPLOY` | `1` | Set to `0` to skip waiting and log streaming (faster return). |
| `COOLIFY_DEPLOY_WAIT_SEC` | `900` | Max seconds to wait for the deployment to finish. |
| `COOLIFY_DEPLOY_POLL_INTERVAL` | `5` | Seconds between status polls. |
| `COOLIFY_LOG_LINES` | `400` | Lines requested for **runtime** logs (build logs are full deployment record). |

To **only** fetch logs for the current app (no deploy), run: `python scripts/coolify_fetch_logs.py`.

Optional `.env` overrides: `DEPLOY_GIT_REPO`, `DEPLOY_GIT_BRANCH`, `COOLIFY_SERVER_UUID` (if multiple servers).

## Preconditions

- Image builds from repo root `Dockerfile` (Python 3.12, Gunicorn, `PORT` default `8080`).
- You have a Coolify instance (often on a Hetzner VPS) with SSH or UI access.
- You generated a **secret** for `FLASK_SECRET_KEY` (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).

## Coolify (high level)

1. **New resource** → build from Git (GitHub `biesdorf-code/sell-tax-free` or your fork) **or** push the image to a registry Coolify can pull from.
2. **Build**: Dockerfile at repository root; context = root.
3. **Ports**: container listens on `$PORT` (default `8080`). Map the public HTTP(S) port Coolify expects to that container port.
4. **Environment**:
   - `FLASK_SECRET_KEY` — required for real deployments (session signing).
   - `PORT` — optional; Coolify may inject this automatically.
5. **Health**: optional HTTP check on `/` (GET returns 200).

## After deploy

- Open the production URL in Chrome, upload a non-sensitive test CSV, verify tax-free / waiting tables and bubble timeline.
- Confirm **no** price columns appear in the UI (NFR-002).

## Rollback

- In Coolify, redeploy the previous successful deployment or pin the prior Git SHA / image digest.
