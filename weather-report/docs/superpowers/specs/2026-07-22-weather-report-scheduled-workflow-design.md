# 定时天气报告工作流设计

## 目标

通过 GitHub Actions 每 15 分钟运行一次天气报告脚本，生成 CSV 报告，并将报告作为 Actions Artifact 提供下载。工作流不向仓库提交或推送任何生成文件。

## 工作流

新增 `.github/workflows/weather-report.yml`，包含两种触发方式：

- 定时触发：`*/15 * * * *`。
- 手动触发：`workflow_dispatch`，便于按需验证或补跑。

每次运行使用 Ubuntu 托管运行器和 Python 3.11，检出当前仓库代码，安装 `requests`，然后执行 `python main.py`。

## 数据与产物

现有脚本会将数据写到 `reports/<YYYY-MM-DD>/weather_report.csv`。工作流在执行完成后上传整个 `reports/` 目录，Artifact 名称为 `weather-reports`，保留 7 天。

Artifact 上传步骤使用 `if: always()`：即使数据拉取或脚本执行失败，也会尝试保存已经生成的报告，方便排查。若没有可上传的报告，工作流继续以脚本本身的成功或失败状态为准。

## 失败行为

依赖安装、天气接口请求或脚本执行失败时，GitHub Actions 将该次运行标记为失败，完整日志可在对应运行记录中查看。该范围不修改现有 Python 代码，也不引入重试逻辑。

## 验证

实现后将：

1. 检查工作流 YAML 的结构与触发配置。
2. 在本地安装依赖并运行 `python main.py`，确认生成 CSV。
3. 确认工作流不包含 git add、commit 或 push 步骤。
