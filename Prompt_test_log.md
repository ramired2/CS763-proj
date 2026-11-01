# Prompt Test Log

## Test 001 — Basic Python addition function

- **Date/time:** 2026-10-31 17:50 (local time)
- **Purpose:** Check whether the assistant generates a basic Python function.
- **Environment/configuration:** See `Agent_environment.md`; exact model and runtime parameters are not exposed.
- **Starting state:** New conversation prompt; no code context supplied.
- **Prompt submitted:**
  ```text
  Write a basic python function names add that returns the sum of two numbers
  ```
- **Expected behavior:** Return a Python function named `add` that returns the sum of two numbers.
- **Observed behavior:**
  ```python
  def add(a, b):
      return a + b
  ```
- **Result:** Pass
- **Validation/evidence:** The response defines `add(a, b)` and returns `a + b`. No code was run.
- **Notes:** None.

## Test 002 — Trivy dependency scan and Semgrep SAST

- **Date/time:** 2026-10-31 18:12 (local time)
- **Purpose:** Configure GitHub Actions to scan dependencies for known vulnerabilities with Trivy and run static application security testing with Semgrep.
- **Environment/configuration:** Python/FastAPI project; see `Agent_environment.md`. Exact model and runtime parameters are not exposed.
- **Starting state:** Barebone FastAPI app, Docker configuration, and DevSecOps GitHub Actions workflow were present.
- **Prompt submitted:**
  ```text
  When scanning dependencies for known vulnerabilities use Trivy and execute static application security testing with Semgrep
  ```
- **Expected behavior:** Use Trivy for dependency vulnerability scanning and Semgrep for SAST in the GitHub Actions pipeline.
- **Observed behavior:** Updated `.github/workflows/devsecops.yml` with a Trivy filesystem vulnerability scan that fails on high/critical findings with available fixes, and a Semgrep Python scan of `app` and `tests`. Updated `requirements-dev.txt` to include Semgrep and remove Bandit and pip-audit.
- **Result:** Pass
- **Validation/evidence:** Semgrep completed with zero findings. Tests (1 passed), Ruff lint/format checks, workflow YAML parsing, and `git diff --check` passed. Trivy is configured as a GitHub Action but was not run locally.
- **Notes:** Trivy will execute when the workflow runs on GitHub Actions.