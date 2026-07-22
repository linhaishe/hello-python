# Weather Report Monorepo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Convert the repository into a monorepo whose first independently runnable application is apps/weather-report, with that application owning its CI steps.

**Architecture:** Move the existing source files unchanged into apps/weather-report/. The root GitHub workflow only supplies GitHub-required triggers, Runner selection, and checkout; it calls a Composite Action located inside the weather application. That action sets up Python, runs the report, and uploads its Artifact.

**Tech Stack:** Python 3.11, requests, GitHub Actions, Composite Actions, actions/checkout@v4, actions/setup-python@v5, actions/upload-artifact@v4.

## Global Constraints

- Use apps/weather-report/ as the application directory.
- Preserve existing weather-fetching, parsing, and CSV-generation behavior and format.
- The schedule is exactly */15 * * * *; manual dispatch is supported.
- Triggerable workflow YAML belongs in .github/workflows/; weather CI steps belong in apps/weather-report/.github/actions/ci/action.yml.
- Use Python 3.11 and install only requests.
- Upload apps/weather-report/reports/ as weather-reports, retain for seven days, and attempt upload after report generation fails.
- CI must never add, commit, push, or otherwise write generated reports to the repository.

## File Structure

- Create README.md: monorepo overview.
- Create apps/weather-report/README.md: project usage.
- Move main.py, constants.py, api/weather.py, services/parser.py, and services/report.py to apps/weather-report/.
- Create apps/weather-report/.github/actions/ci/action.yml: weather-owned Composite Action.
- Create .github/workflows/weather-report.yml: root dispatcher.

---

### Task 1: Move and document the Weather Report application

**Files:**

- Create: README.md
- Create: apps/weather-report/README.md
- Move: main.py, constants.py, api/weather.py, services/parser.py, services/report.py
- Test: the application command run from apps/weather-report/

**Interfaces:**

- Consumes: relative imports api.weather, services.report, and constants.
- Produces: python3 main.py, run from apps/weather-report/, writes reports/<YYYY-MM-DD>/weather_report.csv.

- [ ] **Step 1: Move all application files with Git-aware renames**

~~~bash
mkdir -p apps/weather-report/api apps/weather-report/services
git mv main.py constants.py apps/weather-report/
git mv api/weather.py apps/weather-report/api/
git mv services/parser.py services/report.py apps/weather-report/services/
rmdir api services
~~~

Expected: git status --short shows the five source files under apps/weather-report/.

- [ ] **Step 2: Write the root README**

Write README.md:

~~~markdown
# Hello Python Monorepo

This repository contains independently runnable Python applications.

## Applications

| Application | Description | Run |
| --- | --- | --- |
| [weather-report](apps/weather-report/README.md) | Fetches weather data and writes a CSV report. | cd apps/weather-report && python3 main.py |

## Repository layout

~~~text
apps/       # Independently runnable applications
.github/    # GitHub Actions dispatchers
~~~
~~~

- [ ] **Step 3: Write the application README**

Write apps/weather-report/README.md:

~~~markdown
# Weather Report

Fetches weather data for the configured cities and writes a CSV report.

## Run locally

~~~bash
python -m pip install requests
python3 main.py
~~~

Run these commands from apps/weather-report/. The report is written to reports/<YYYY-MM-DD>/weather_report.csv.
~~~

- [ ] **Step 4: Verify the application from its new working directory**

Run:

~~~bash
cd apps/weather-report && python3 -m pip install requests && python3 main.py && find reports -type f -name weather_report.csv -print
~~~

Expected: output includes reports/<YYYY-MM-DD>/weather_report.csv.

- [ ] **Step 5: Review and commit the application move**

~~~bash
git diff --check
git add README.md apps/weather-report
git commit -m "refactor: move weather report into apps"
~~~

Expected: no whitespace error; the commit contains the application moves and both READMEs.

### Task 2: Add the weather-owned Composite Action and root dispatcher

**Files:**

- Create: apps/weather-report/.github/actions/ci/action.yml
- Create: .github/workflows/weather-report.yml
- Test: static Python assertions over both YAML files

**Interfaces:**

- Consumes: a checked-out workspace containing apps/weather-report.
- Produces: a local Composite Action invoked as ./apps/weather-report/.github/actions/ci.

- [ ] **Step 1: Write and run a red-capable static check before implementation**

~~~bash
python - <<'PY'
from pathlib import Path
assert Path('.github/workflows/weather-report.yml').is_file(), 'missing root workflow dispatcher'
assert Path('apps/weather-report/.github/actions/ci/action.yml').is_file(), 'missing weather CI composite action'
PY
~~~

Expected: failure containing missing root workflow dispatcher.

- [ ] **Step 2: Create the weather project Composite Action**

Write apps/weather-report/.github/actions/ci/action.yml:

~~~yaml
name: Run Weather Report CI
description: Install dependencies, generate a weather report, and upload it as an artifact.

runs:
  using: composite
  steps:
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install dependencies
      shell: bash
      working-directory: ${{ github.workspace }}/apps/weather-report
      run: python -m pip install requests

    - name: Generate weather report
      shell: bash
      working-directory: ${{ github.workspace }}/apps/weather-report
      run: python main.py

    - name: Upload weather reports
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: weather-reports
        path: apps/weather-report/reports/
        retention-days: 7
        if-no-files-found: warn
~~~

- [ ] **Step 3: Create the root workflow dispatcher**

Write .github/workflows/weather-report.yml:

~~~yaml
name: Weather Report

on:
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:

jobs:
  weather-report:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run weather report CI
        uses: ./apps/weather-report/.github/actions/ci
~~~

- [ ] **Step 4: Re-run static workflow assertions**

~~~bash
python - <<'PY'
from pathlib import Path
dispatcher = Path('.github/workflows/weather-report.yml').read_text()
action = Path('apps/weather-report/.github/actions/ci/action.yml').read_text()
assert '*/15 * * * *' in dispatcher
assert 'workflow_dispatch:' in dispatcher
assert 'runs-on: ubuntu-latest' in dispatcher
assert 'uses: ./apps/weather-report/.github/actions/ci' in dispatcher
assert 'using: composite' in action
assert 'actions/setup-python@v5' in action
assert 'python-version: "3.11"' in action
assert 'working-directory: ${{ github.workspace }}/apps/weather-report' in action
assert 'run: python main.py' in action
assert 'path: apps/weather-report/reports/' in action
assert 'retention-days: 7' in action
assert 'if: always()' in action
assert 'git add' not in dispatcher + action
assert 'git commit' not in dispatcher + action
assert 'git push' not in dispatcher + action
print('Workflow configuration checks passed')
PY
~~~

Expected: Workflow configuration checks passed.

- [ ] **Step 5: Review and commit the CI boundary**

~~~bash
git diff --check
git add .github/workflows/weather-report.yml apps/weather-report/.github/actions/ci/action.yml
git commit -m "ci: delegate weather workflow to app action"
~~~

Expected: no whitespace error; the commit contains only the root dispatcher and the Composite Action.

### Task 3: Final verification

**Files:**

- Verify: README.md, apps/weather-report/, .github/workflows/weather-report.yml, and apps/weather-report/.github/actions/ci/action.yml

**Interfaces:**

- Consumes: the migrated application and the dispatcher/action pair.
- Produces: a verified monorepo layout with project-owned CI steps.

- [ ] **Step 1: Verify required paths**

~~~bash
test -f apps/weather-report/main.py
test -f apps/weather-report/constants.py
test -f apps/weather-report/api/weather.py
test -f apps/weather-report/services/parser.py
test -f apps/weather-report/services/report.py
test -f apps/weather-report/.github/actions/ci/action.yml
test -f .github/workflows/weather-report.yml
printf 'Monorepo layout checks passed\n'
~~~

Expected: Monorepo layout checks passed.

- [ ] **Step 2: Verify the documented application command**

~~~bash
cd apps/weather-report && python3 main.py && test -f "reports/$(date +%F)/weather_report.csv" && printf 'Weather report execution check passed\n'
~~~

Expected: Weather report execution check passed.

- [ ] **Step 3: Verify final Git state**

~~~bash
git diff --check
git status --short
git log -2 --oneline
~~~

Expected: no whitespace errors; the two implementation commits are visible and no generated report directory is staged.
