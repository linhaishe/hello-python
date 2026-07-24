# Weather Report

Fetches weather data for the configured cities and writes a CSV report.

## 多源 API 数据抓取与本地报表生成器（以天气/财经/热搜为例）

> **场景**：每天自动去网上调 API 抓取数据，清洗汇总后保存为本地 CSV 文件，并按日期自动创建文件夹归档。

### 核心功能步骤：

1. **网络请求 (`requests`)**：
   - 调用免费的公开 API（比如某个天气 API、聚合热搜 API、或者加密货币价格 API）。
   - 甚至可以用 `requests` 访问几个网页提取 JSON 响应。
2. **数据解析 (`json` / `csv`)**：
   - 用 `response.json()` 提取出你关心的关键字段（比如：城市、温度、天气状况、更新时间）。
   - 使用 Python 自带的 `csv` 模块，把这些结构化数据追加写入到本地的 `weather_report.csv` 中。
3. **文件与系统自动化 (`os` / `sys`)**：(WIP)
   - 使用 `sys.argv` 允许用户从命令行传入参数（例如指定城市或导出文件名：`python main.py --city Beijing`）。
   - 用 `os.path.exists()` 检查今天日期的文件夹是否存在（如 `./reports/2026-07-20/`），如果不存在，用 `os.makedirs()` 自动创建文件夹并将 CSV 存入其中。

## Run locally

```bash
python -/m pip install requests
python3 apps/weather-report/main.py
```

Run these commands from apps/weather-report/. The reports are written to reports/<YYYY-MM-DD>/, including:
- `weather_report.csv`
- `weather_report.db` (SQLite)

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