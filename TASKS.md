# Tasks

I sequence work against `REQUIREMENTS.md` and `SPEC.md`; I do not define product behavior in this file.

| Task | Goal I execute | Files I use | Criteria I verify |
|---|---|---|---|
| T-01 | I configure package, demo data and environment. | `pyproject.toml`, `README.md`, `data.py` | AC-08, AC-09 |
| T-02 | I define the immutable customer model and enforce its existing ID invariant. | `models.py`, `tests/test_model_validation.py` | AC-04, AC-10 |
| T-03 | I implement unified partial casefold matching. | `search.py`, `tests/test_search.py` | AC-01, AC-02, AC-03 |
| T-04 | I implement CLI, validation and errors. | `cli.py`, `__main__.py`, `tests/test_cli.py` | AC-04, AC-05, AC-06 |
| T-05 | I retain and extend behavior tests. | `tests/` | AC-07, AC-10 |
| T-06 | I document usage, traceability and observed evidence. | `README.md`, `docs/traceability.md`, `results/`, `AI_USAGE_LOG.md` | AC-08, AC-09 |
| T-08 | I improve context, navigation, guardrails and CI without changing product code before AFTER. | `AGENTS.md`, `docs/REPO_MAP.md`, `scripts/`, `.github/workflows/verify.yml` | I use repository checks rather than new product AC. |

## Controlled Change

I select T-02 / CR-ADA08-01 in `TASK_UNDER_TEST.md`. I implement the same task from the same functional baseline in both worktrees. I preserve the BEFORE patch as evidence and use only the AFTER implementation in the final active source tree.

## ADA-09 Work Sequence

I execute T-09.1 approved contract preparation; T-09.2 isolated coder implementation of FR-07 / AC-11 through AC-15; T-09.3 deterministic verification; T-09.4 independent read-only review; T-09.5 human finding decisions; T-09.6 accepted fixes if required; T-09.7 independent re-review; and T-09.8 final human readiness decision and PR evidence. I keep the original ADA-08 tasks as historical context.
