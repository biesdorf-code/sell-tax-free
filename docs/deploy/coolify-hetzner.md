# Deploy Sell Tax Free — Coolify on Hetzner

Operational companion to the in-app **Deploy to production?** gate (`/deploy`).

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
