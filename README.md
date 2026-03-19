# CI Pipeline with DevSecOps Controls

**CYOM 569** — Continuous integration with quality and security gates for a minimal Flask application.

[![CI Pipeline](https://github.com/ivanofmg/cyom569-project-task-2-ci-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanofmg/cyom569-project-task-2-ci-pipeline/actions/workflows/ci.yml)

## Tech stack

Inspired by portfolio-style READMEs: **[Shields.io](https://shields.io/)** badges with **`style=for-the-badge`** (bold, high-contrast blocks), **ALL CAPS** labels, and [Simple Icons](https://simpleicons.org/) where the logo is stable.

### 🔄 CI/CD & version control

[![GitHub Actions](https://img.shields.io/badge/GITHUB%20ACTIONS-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Git](https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)
[![GitHub](https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

### 🐍 Runtime & application

[![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/FLASK-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Markdown](https://img.shields.io/badge/MARKDOWN-000000?style=for-the-badge&logo=markdown&logoColor=white)](https://daringfireball.net/projects/markdown/)

### 🐳 Containerization

[![Docker](https://img.shields.io/badge/DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

### 🛡️ Quality & security (DevSecOps)

[![flake8](https://img.shields.io/badge/FLAKE8-00979D?style=for-the-badge)](https://flake8.pycqa.org/)
[![Bandit](https://img.shields.io/badge/BANDIT-EAB403?style=for-the-badge&logo=python&logoColor=black)](https://bandit.readthedocs.io/)

> **How to customize:** edit label text or hex colors in the badge URL (`MESSAGE-COLOR` segment), or browse presets at [shields.io/badges](https://shields.io/badges). Add tools by duplicating a badge row and picking `logo=` from Simple Icons slugs.

### Quick reference (versions)

| Area | Choice |
|------|--------|
| Runtime | Python **3.11**, **Flask** 3.x |
| Container | **Docker** (`python:3.11-slim`) |
| CI/CD | **GitHub Actions** |
| Linting | **flake8** |
| Security (SAST) | **Bandit** |

---

## Summary

This repository implements a **GitHub Actions CI pipeline** that validates Python code, enforces style with **flake8**, runs **SAST** with **Bandit**, and verifies a **Docker** image build on every change to `main`. The design follows **shift-left** and **DevSecOps** practices described in resources such as *Hands-On Security in DevOps*.

| Goal | How it is met |
|------|----------------|
| Fast feedback | Automated checks on push and pull requests |
| Code quality | flake8 as a failing gate |
| Security posture | Bandit on application source; sensible defaults for bind address |
| Reproducibility | Docker image build in CI; pinned dependencies |

---

## Architecture

```text
Developer
    → git push / pull request (branch: main)
        → GitHub Actions: build-and-validate
            1. Checkout + Python 3.11
            2. Install dependencies + flake8 + bandit
            3. Syntax: py_compile
            4. Lint: flake8
            5. SAST: bandit
            6. Build: docker build
```

---

## Application

Small HTTP service:

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Welcome message |
| `GET /health` | JSON health check (`200`) |

### Configuration

Runtime listen address and port are **environment-driven** (avoids hardcoding `0.0.0.0` in source, which tools such as Bandit flag as **B104**):

| Variable | Default | Notes |
|----------|---------|--------|
| `HOST` | `127.0.0.1` | Safe default for local development |
| `PORT` | `5000` | |

The **Dockerfile** sets `HOST=0.0.0.0` so the container accepts external traffic as expected in containerized deployments.

---

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
set HOST=127.0.0.1              # optional; defaults apply
python app.py
```

---

## Docker

```bash
docker build -t cyom569-ci-pipeline .
docker run --rm -p 5000:5000 cyom569-ci-pipeline
```

Then open `http://127.0.0.1:5000` and `http://127.0.0.1:5000/health`.

---

## CI pipeline (workflow)

**Triggers:** `push` and `pull_request` targeting `main`.

**Job:** `build-and-validate` on `ubuntu-latest`.

| Step | Command / action |
|------|------------------|
| Checkout | `actions/checkout@v4` |
| Python | `actions/setup-python@v5` → 3.11 |
| Dependencies | `pip install -r requirements.txt` + `flake8` + `bandit` |
| Syntax | `python -m py_compile app.py` |
| Lint | `flake8 . --count --statistics` |
| Security | `bandit -r . -ll -x .venv -x venv` |
| Image | `docker build -t cyom569-ci-pipeline .` |

**Bandit exclusions:** `.venv` and `venv` are excluded so local virtualenv trees (if present) do not pollute results with third-party code.

---

## DevSecOps controls (at a glance)

- **Quality gate:** pipeline fails on flake8 violations (e.g. PEP 8 line length **E501**).
- **Security gate:** Bandit fails the job on configured severity; **B104** addressed via env-based `HOST` + Dockerfile `ENV`.
- **Secure configuration:** no hardcoded bind-all interface in application source; twelve-factor style env config.
- **Build verification:** Docker image must build successfully in CI.

---

## Repository layout

```text
.
├── app.py                 # Flask application
├── requirements.txt       # Pinned Flask dependency
├── Dockerfile             # Container image + HOST/PORT for runtime
├── .github/workflows/
│   └── ci.yml             # GitHub Actions workflow
└── docs/
    └── BITACORA.md        # Technical project log (Spanish)
```

---

## Roadmap

- Dependency scanning (e.g. **pip-audit**)
- Container image scanning (e.g. **Trivy**)
- Automated tests (pytest) in CI
- Optional CD stage (deploy)

---

## Author

**Ivanof Mercado** — Cybersecurity & DevOps

---

## License / course context

Project work for **CYOM 569**. Adjust licensing here if you publish the repo publicly.
