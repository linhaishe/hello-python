# Weather Report

Fetches weather data for the configured cities and writes a CSV report.

## Run locally

```bash
python -m pip install requests
python3 main.py
```

Run these commands from apps/weather-report/. The report is written to reports/<YYYY-MM-DD>/weather_report.csv.

```
name: Weather Report

on:
  push:
    branches: [main, daily/cicd]
    paths:
      - 'apps/weather-report/**'
      - '.github/workflows/weather-report.yml'
  pull_request:
    branches: [main, daily/cicd]
    paths:
      - 'apps/weather-report/**'
      - '.github/workflows/weather-report.yml'
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:

jobs:
  weather-report-steps: &weather-report-steps
    - name: Check out repository
      uses: actions/checkout@v4

    - name: Run weather report CI
      uses: ./apps/weather-report/.github/actions/ci

  weather-report-push:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps: *weather-report-steps

  weather-report-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps: *weather-report-steps

  weather-report-schedule:
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps: *weather-report-steps
```

```
jobs:
  weather-report-push:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run weather report CI
        uses: ./apps/weather-report/.github/actions

  weather-report-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run weather report CI
        uses: ./apps/weather-report/.github/actions/ci

  weather-report-schedule:
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run weather report CI
        uses: ./apps/weather-report/.github/actions
```
里面的路径是：

```
today = datetime.now().strftime("%Y-%m-%d")
folder = f"./reports/{today}"
filename = f"{folder}/weather_report.csv"
```

而你的 action 里设置了：

`working-directory: ${{ github.workspace }}/apps/weather-report`
所以 `./reports/...` 实际上就是相对于 `apps/weather-report/` 这个目录。

最终落盘位置就是：
`apps/weather-report/reports/2026-07-22/weather_report.csv`