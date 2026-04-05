# Cloud CI/CD Project (GitHub Actions + Docker + GHCR + OCI VM)

A portfolio project demonstrating an end-to-end CI/CD pipeline for a Python (Flask) service deployed as a Docker container to an Oracle Cloud Infrastructure (OCI) Ubuntu VM.

---

## What this project demonstrates (DevOps/SRE skills)

- **CI quality gates** on pull requests and pushes:
  - Linting with `ruff`
  - Unit tests with `pytest`
- **Artifact build**:
  - Docker image built on pushes/merges to `main`
- **Artifact publishing**:
  - Image pushed to **GitHub Container Registry (GHCR)** with:
    - immutable tag: commit SHA
    - mutable tag: `latest`
- **Continuous delivery**:
  - Deploys to an **OCI Compute VM** via SSH
  - Pulls the exact SHA-tagged image and restarts the service container
- **Operational readiness**:
  - `/healthz` endpoint used as a readiness gate during deploy
  - `/version` endpoint returns the deployed version (commit SHA passed via env var)
  - Deployment includes retries and prints container logs on failure
- **Rollback**:
  - Manual workflow trigger can redeploy any previously built SHA image tag

---

## Architecture (high level)

1. **Pull request opened** → GitHub Actions runs CI:
   - `ruff` (lint)
   - `pytest` (tests)

2. **Push/Merge to `main`** → GitHub Actions:
   - builds a Docker image
   - pushes to GHCR:
     - `ghcr.io/<owner>/cloud-ci-cd-project:<sha>`
     - `ghcr.io/<owner>/cloud-ci-cd-project:latest`

3. **Deploy job** (on `main` push, or manual dispatch):
   - SSH into OCI VM
   - `docker pull` the selected image tag (default: current SHA)
   - restart container `cicd-demo`
   - wait for `GET /healthz` to succeed
   - print `GET /version` to verify deployed version

---

## Endpoints

- `GET /` → `CI/CD Pipeline is working!`
- `GET /healthz` → `{"status":"ok"}`
- `GET /version` → `{"version":"<sha-or-unknown>"}`

---

## Repo structure

```text
cloud-ci-cd-project/
  app/
    main.py
    requirements.txt
    tests/
  terraform/
    *.tf (infrastructure as code scaffolding)
  .github/
    workflows/
      ci-cd-v2.yml
  pytest.ini
  README.md
