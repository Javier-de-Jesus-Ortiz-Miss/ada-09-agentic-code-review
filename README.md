# Customer Search - ADA-09 Agentic Code Review

I copied my agent-ready ADA-08 repository into an independent project and preserved its source provenance, verification scripts and technical history. I develop CR-ADA09-01 through separate coder, reviewer, human-decision and re-review stages.

## Start Here

I use [AGENTS.md](AGENTS.md), [CHANGE_REQUEST.md](CHANGE_REQUEST.md), [requirements](REQUIREMENTS.md), [specification](SPEC.md), [architecture](ARCHITECTURE.md), [tasks](TASKS.md) and [the repository map](docs/REPO_MAP.md) as my navigation path.

## Installation

I use Python 3.11+ and install the pinned tools:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
```

## Verification

I run `./scripts/verify_repo.sh` for tests, Ruff, repository integrity and security pattern checks. I use `PYTHON=/absolute/path/to/python ./scripts/verify_repo.sh` with an existing environment. I keep the same gate in GitHub Actions on Python 3.11 and 3.13.

## Review Workflow

I preserve `main` as the review baseline and implement the approved Change Request on `ada09/cr-search-field`. I retain the actual Pull Request and the reports under `results/`. I keep the human readiness decision separate from green tests and reviewer recommendations. I do not merge automatically.

## Historical Context

I preserve the inherited ADA-08 BEFORE/AFTER artifacts as earlier evidence. I use the ADA-09 run context, coder report, verification report, review contract, independent findings, human decisions, re-review and PR evidence for this activity. I retain technical decisions in AI_USAGE_LOG without personal dialogue or transcripts.
