# Scheduled Weather Report Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a GitHub Actions workflow that fetches weather data every 15 minutes and makes generated CSV reports downloadable without modifying the repository.

**Architecture:** A single workflow file runs on GitHub-hosted Ubuntu runners. It checks out the repository, installs the existing runtime dependency, runs the existing `main.py` entry point, and uploads `reports/` as an expiring artifact. The workflow has no git write operations.

**Tech Stack:** GitHub Actions, Ubuntu runner, Python 3.11, `requests`, `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`.

## Global Constraints

- Schedule must be exactly `*/15 * * * *`.
- Include `workflow_dispatch` for manual runs.
- Use Python 3.11.
- Do not add `git add`, `git commit`, `git push`, or repository write permissions.
- Upload `reports/` as artifact `weather-reports` with `retention-days: 7`.
- Attempt artifact upload after both success and failure using `if: always()`.

---

### Task 1: Add the scheduled GitHub Actions workflow

**Files:**
- Create: `.github/workflows/weather-report.yml`
- Test: `.github/workflows/weather-report.yml` (static YAML and content assertions)

**Interfaces:**
- Consumes: repository entry point `main.py`, which writes CSV output beneath `reports/`.
- Produces: the `Weather Report` workflow, available in the GitHub Actions UI and triggered by cron or manual dispatch.

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/weather-report.yml` with exactly:

```yaml
name: Weather Report

on:
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:

jobs:
  fetch-weather-report:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: python -m pip install requests

      - name: Generate weather report
        run: python main.py

      - name: Upload weather reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: weather-reports
          path: reports/
          retention-days: 7
          if-no-files-found: warn
```

- [ ] **Step 2: Validate required workflow behavior**

Run:

```bash
python - <<'PY'
from pathlib import Path

workflow_path = Path('.github/workflows/weather-report.yml')
text = workflow_path.read_text()

assert '*/15 * * * *' in text
assert 'workflow_dispatch:' in text
assert 'runs-on: ubuntu-latest' in text
assert 'git commit' not in text
assert 'git push' not in text
assert 'retention-days: 7' in text
assert 'if: always()' in text
print('Workflow configuration checks passed')
PY
```

Expected: `Workflow configuration checks passed`.

- [ ] **Step 3: Run the existing report generator locally**

Run:

```bash
python -m pip install requests
python main.py
find reports -type f -name weather_report.csv -print
```

Expected: the final command prints at least one `reports/<YYYY-MM-DD>/weather_report.csv` path. The command may add a current-date report directory; leave it untracked because generated reports are not part of this change.

- [ ] **Step 4: Review the staged change**

Run:

```bash
git diff --check
git diff -- .github/workflows/weather-report.yml
git status --short
```

Expected: no whitespace errors; the diff contains only the workflow file, and generated reports remain untracked or are removed from the staging area.

- [ ] **Step 5: Commit the workflow**

Run:

```bash
git add .github/workflows/weather-report.yml
git commit -m "ci: schedule weather report generation"
```

Expected: Git creates a commit containing only `.github/workflows/weather-report.yml`.
