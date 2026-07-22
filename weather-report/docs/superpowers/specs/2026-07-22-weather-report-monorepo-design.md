# Weather Report Monorepo Design

## Goal

Convert this repository into a lightweight monorepo. The existing weather report program becomes the first independently runnable application at `apps/weather-report/`.

## Scope

- Move the current weather report source files into `apps/weather-report/`.
- Add a repository-level overview README and keep an application-specific README beside the application.
- Add a GitHub Actions workflow that runs the application every 15 minutes or on manual dispatch.
- Preserve existing weather-fetching, parsing, and CSV-generation behavior.

No shared package, package manager workspace, repository write permissions, or generated report commits are part of this change.

## Repository Structure

```text
apps/
  weather-report/
    .github/
      actions/
        ci/
          action.yml
    api/
    services/
    constants.py
    main.py
    README.md
.github/
  workflows/
    weather-report.yml
README.md
```

`apps/weather-report` is self-contained and runs with `python main.py` from that directory. Its generated CSV files remain under `apps/weather-report/reports/<YYYY-MM-DD>/`.

The repository root is reserved for cross-project documentation, automation, and future shared packages such as `packages/`.

## CI/CD

GitHub only discovers triggerable workflows in the repository-root `.github/workflows/` directory. Therefore, `.github/workflows/weather-report.yml` is a small project-specific dispatcher. It has two triggers:

- A `*/15 * * * *` schedule.
- `workflow_dispatch` for manual runs.

After checking out the repository, the dispatcher invokes the local Composite Action at `apps/weather-report/.github/actions/ci/action.yml`. That action owns the weather report CI steps: it configures Python 3.11, installs `requests`, executes `python main.py` with `apps/weather-report` as its working directory, and uploads `apps/weather-report/reports/` as a `weather-reports` artifact retained for seven days. The upload runs with `if: always()` so partial output is retained after a failure.

This keeps each subproject's CI steps beside its source code while reserving root workflow files for the GitHub-required trigger and runner declaration. Composite Actions contain steps only; a subproject that later needs multiple jobs, a job matrix, or an independently configured deployment environment will require its own project-named root workflow file.

The workflow does not add, commit, push, or otherwise write generated files to the repository.

## Validation

Validation will confirm:

1. `python main.py` succeeds when run from `apps/weather-report` and writes its CSV beneath that directory.
2. The workflow has the intended schedule, manual trigger, working directory, Artifact path, retention, and no git write commands.
3. The repository has no whitespace errors and the moved application is documented from both the root and application directories.
