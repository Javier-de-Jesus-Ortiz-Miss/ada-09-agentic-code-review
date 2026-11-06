# Repository Map

## Entry Points

I begin at [the approved Change Request](../CHANGE_REQUEST.md), [the review rules](REVIEW_RULES.md), and [the operating contract](../AGENTS.md) and [the README](../README.md). I resolve behavior in [requirements](../REQUIREMENTS.md) and [specification](../SPEC.md), dependencies in [architecture](../ARCHITECTURE.md), sequencing in [tasks](../TASKS.md), and the bounded change in [the fixed task](../TASK_UNDER_TEST.md).

| Question I need to answer | File I inspect |
|---|---|
| How do I launch the CLI? | `src/customer_search/__main__.py`, `pyproject.toml` |
| Where do I parse input and format results? | `src/customer_search/cli.py` |
| Where do I enforce a customer invariant? | `src/customer_search/models.py` |
| Where do I normalize and match queries? | `src/customer_search/search.py` |
| Where are the fictional data? | `src/customer_search/data.py` |
| How do I validate everything? | `scripts/verify_repo.sh` |
| Where do I inspect reproducibility limits? | `docs/EXPERIMENT.md`, `results/evidence/` |
| What did I reuse from ADA-07? | `skills/reviewing_pull_requests/`, `results/prior/ada07/` |

## Tests

- I find query, Unicode, order, no-duplication and generator tests in `tests/test_search.py`.
- I find real subprocess CLI, streams, arguments and exit-code tests in `tests/test_cli.py`.
- I find CR-ADA08-01 constructor and immutability regressions in `tests/test_model_validation.py` after implementing the task.
- I find adversarial mutations of the repository contract in `tests/test_repo_contract.py`.
- I map each FR/AC to tests in [my traceability matrix](traceability.md).

## Change Guide

I read the relevant requirement and AC first. For identifier validation, I edit only `models.py` and add focused tests in `test_model_validation.py`. For query behavior, I inspect `search.py` and its tests before changing matching. For CLI behavior, I inspect `cli.py` and subprocess tests. I require a human decision before expanding scope, architecture or normative product behavior. I run `./scripts/verify_repo.sh`, inspect `git diff`, and retain actual evidence.

## Do Not Edit Directly

I do not modify `results/prior/`, `skills/`, `src/customer_search/data.py`, `TASK_UNDER_TEST.md`, `docs/EXPERIMENT_PROMPT.txt`, or baseline evidence listed in `docs/protected-paths.json`. I regenerate `outputs/` archives through the packaging script. I do not store or edit `.env`, private keys, credentials, production configuration, `.git/` internals or dependency caches. I use ordinary Git commands for history and never rewrite the baseline tag.

## Scope of Local Contracts

I apply root `AGENTS.md` across the active repository. I keep inherited contracts under `results/prior/` as historical evidence, outside active source navigation. I preserve the ADA-07 skill as a reusable local reference under `skills/`; I do not install a third-party collection or activate unrelated skills during this task.

## ADA-09 Review Navigation

I inspect search.py and cli.py for field selection and the new focused test modules for domain and CLI behavior. I locate the full review cycle in results/run-context.md, coder-report.md, verification-report.md, pr.diff, commits.txt, review-contract.md, review-report.md, human-review-decisions.md, re-review-report.md and PR_EVIDENCE.md. I use CHANGE_REQUEST as my active task and preserve TASK_UNDER_TEST as historical ADA-08 evidence.
