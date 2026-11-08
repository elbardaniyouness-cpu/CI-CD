# CI/CD Final Project – Counter Service

**Project name:** CI/CD Final Project – Counter Service
**Author:** Youness El Bardani
**Course:** Continuous Integration and Continuous Delivery (CI/CD) – Coursera Final Project

This project builds and deploys a complete CI/CD pipeline for a small Python Flask
microservice (the **Counter Service**). Code is linted and tested on every push with
**GitHub Actions**, and built and deployed to an **OpenShift** cluster by a
**Tekton / OpenShift Pipeline**.

## The application

A REST API that keeps named counters in memory.

| Method | Endpoint           | Description         |
|--------|--------------------|---------------------|
| GET    | `/health`          | Health check        |
| GET    | `/`                | Service information |
| GET    | `/counters`        | List all counters   |
| POST   | `/counters/<name>` | Create a counter    |
| GET    | `/counters/<name>` | Read a counter      |
| PUT    | `/counters/<name>` | Increment a counter |
| DELETE | `/counters/<name>` | Delete a counter    |

## Repository layout

```
.github/workflows/workflow.yml   GitHub Actions CI: lint with flake8, run unit tests with nose
.tekton/tasks.yml                Custom Tekton tasks: cleanup, nose
.tekton/pipeline.yml             OpenShift pipeline "oc-final"
.tekton/pvc.yml                  PersistentVolumeClaim used as the pipeline workspace
service/                         Flask application source
tests/                           Unit tests
Dockerfile                       Container image (gunicorn on port 8000)
requirements.txt                 Python dependencies
setup.cfg                        flake8 / nose / coverage settings
```

## Continuous Integration (GitHub Actions)

`.github/workflows/workflow.yml` runs on every push and pull request to `main`
inside a `python:3.9-slim` container:

1. **Checkout**
2. **Install dependencies**
3. **Lint with flake8**
4. **Run unit tests with nose** (with coverage)

## Tekton tasks

- **cleanup** – empties the shared workspace before each run
- **nose** – installs requirements and runs `nosetests`

The pipeline also uses the cluster tasks **git-clone**, **flake8**, **buildah**
and **openshift-client**.

## OpenShift Pipeline (`oc-final`)

```
cleanup -> git-clone -> flake8 ─┐
                     └-> nose ──┴-> buildah -> deploy
```

## Running locally

```bash
python3.9 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flake8 service
nosetests -v --with-spec --spec-color --with-coverage --cover-package=service
gunicorn --bind=0.0.0.0:8000 service:app
```

## Technologies

Python 3.9 · Flask · gunicorn · flake8 · nose · GitHub Actions · Tekton ·
OpenShift Pipelines · Buildah
