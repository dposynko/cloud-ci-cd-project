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


## Local development
## Create venv + run checks

cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest ruff
ruff check .
pytest -q

## Run the app locally

python main.py
# in another terminal:
curl http://localhost:5000/healthz

## Docker (local)

cd app
docker build -t cicd-demo:local .
docker run --rm -p 5000:5000 cicd-demo:local

curl http://localhost:5000/
curl http://localhost:5000/healthz
curl http://localhost:5000/version


## OCI VM prerequisites
Ubuntu VM reachable via SSH (user typically ubuntu)
Docker installed on the VM (workflow can install it automatically, but pre-install is fine)
OCI network rules allow:
inbound TCP/22 for SSH (ideally restricted)
inbound TCP/5000 from your IP (only if you want to access the app externally)

## GitHub Actions secrets required
Repo → Settings → Secrets and variables → Actions → Repository secrets

OCI_HOST : OCI VM public IP (e.g., 203.0.113.10)
OCI_USER : ubuntu
OCI_SSH_KEY : private SSH key used to SSH into the VM (use a dedicated deploy keypair)
Security note: never commit keys to git. Rotate keys if they are exposed.

## CI/CD workflow (v2)
Workflow file: .github/workflows/ci-cd-v2.yml

Automatic deploy
Trigger: push/merge to main
Builds image, pushes to GHCR, deploys to OCI VM
Manual deploy / rollback
GitHub → Actions → “CI/CD v2 (GHCR -> OCI VM)” → Run workflow
Optional input:
image_tag: a previous commit SHA tag to redeploy (rollback)

## Troubleshooting
On the VM: check container status and logs

sudo docker ps -a --filter name=cicd-demo
sudo docker logs --tail 200 cicd-demo

## Verify locally on the VM

curl -v http://localhost:5000/healthz
curl -v http://localhost:5000/version

## Common issues
Secrets missing in Actions: secret names must match exactly (OCI_HOST, OCI_USER, OCI_SSH_KEY)
Health check flakiness right after restart: the workflow uses retries to wait for readiness
GHCR image pull failures: if the package is private, the VM needs GHCR auth or the package must be public
