# Deployments and containers

**2026-04-24** — Sprint 2 capitalization, integrated from `docs/sprints/sprint-02/compound.md`.

## Concepts

- **PORT and Gunicorn:** Production images should honor `PORT` for PaaS; the same image can be exercised locally with `docker run -p`.
- **In-container health checks:** Platforms often run `curl` or `wget` inside the container. Slim bases may omit both; install a client or change the health check.
- **Edge routing:** When the service listens on a non-default port (e.g. 8080), the public URL may need that port so Traefik/Coolify routing matches the load balancer.

## Practical example

Dockerfile: install `curl` when Coolify uses an HTTP probe; bind Gunicorn to `0.0.0.0` and the configured `PORT`.
