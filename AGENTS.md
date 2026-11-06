# Agent Operating Contract - ADA-09

## Read First

I read `CHANGE_REQUEST.md`, `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, and `docs/REPO_MAP.md`. I use `docs/REVIEW_RULES.md` for independent review. I treat inherited ADA-08 reports as historical evidence rather than new authority.

## Sources of Truth

I keep requirements in `REQUIREMENTS.md`, behavior and acceptance criteria in `SPEC.md`, dependency boundaries in `ARCHITECTURE.md`, and sequencing in `TASKS.md`. I use `CHANGE_REQUEST.md` to select already-defined requirements. I never change normative behavior merely to make code or tests pass.

## Repository Map

I use `src/customer_search/search.py` for query rules and field selection, `cli.py` for arguments and presentation, `models.py` for immutable customer records, and `data.py` for fictional read-only data. I keep tests in `tests/`, checks in `scripts/`, review evidence in `results/`, and review guidance in `docs/REVIEW_RULES.md`.

## Standard Commands

I install with `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements-dev.txt`, and `.venv/bin/python -m pip install --no-deps --no-build-isolation -e .`.

I run `PYTHONPATH=src python3 -m customer_search ana`. I use `.venv/bin/python -m pytest -q` for tests, `.venv/bin/python -m ruff check src tests scripts` for lint, `.venv/bin/python scripts/check_repo_contract.py` for contracts, and `.venv/bin/python scripts/check_security.py` for the security pattern check. I use `./scripts/verify_repo.sh` as the shared gate, with `PYTHON=/absolute/path/to/python` when needed.

I run `.venv/bin/python scripts/check_review_evidence.py --phase final` only after independent review, decisions and re-review are complete. A green code gate does not substitute for a human decision.

## Change Rules

I scope CR-ADA09-01 production edits to `src/customer_search/search.py` and `src/customer_search/cli.py`. I add focused tests in `tests/test_search_fields.py` and `tests/test_cli_fields.py`; I retain existing tests unchanged. I allow the coder to update feature usage and `results/coder-report.md`. I keep runtime dependencies empty and preserve the original two-argument search call.

I preserve `results/prior/`, `skills/`, fictional data and the inherited protected inputs under `docs/protected-paths.json`. I keep the ADA-08 controlled task as historical evidence and do not apply its old product-edit scope to this approved ADA-09 change.

## Role Separation

I require delegation to separate coder and reviewer subagents with fresh contexts and no inherited conversation history. I keep the coordinator responsible for contracts, deterministic execution, Git metadata and publication. I do not let the coder approve its implementation.

I give the reviewer only repository context, the candidate diff, actual source/tests and verification evidence. I allow the reviewer to write only review reports and isolated probe evidence; I prohibit production-code, test or requirement edits during the initial review. I check source/test hashes before and after that review. I use a separate re-review to assess resolutions. I retain structured findings and decisions without personal questions, transcripts or conversational metadata.

## Safety and Permissions

I permit the coordinator to create the new public ADA-09 repository, push its branches and tags, and create/update the required Pull Request under the project authorization. I leave ADA-08 unchanged. I prohibit agents from merging, approving their own PR, writing GitHub review comments or sending messages to people. I exclude secrets, credentials, production settings and private keys. I treat static pattern checks as bounded detection, not complete secret or security auditing.

## Stop Conditions

I stop on conflicting requirements, an unapproved Change Request, destructive work outside this repository, new dependencies without justification, protected evidence changes, or an unavailable required system. I record human gates only after actual approval. I leave accepted MUST FIX findings open until an independent re-review confirms their resolution.

## Definition of Done

I preserve the base and candidate commits, run the shared gate, obtain independent findings with evidence, record actual human decisions, resolve accepted blockers and complete re-review. I create the ten required result artifacts, retain at least six technical AI log entries and link the real PR. I require an explicit final human readiness decision before marking READY FOR HUMAN MERGE; I do not merge automatically.
