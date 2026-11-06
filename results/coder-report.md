# My CR-ADA09-01 Coder Report

## Change

Change ID: CR-ADA09-01
Branch: ada09/cr-search-field
Base commit: 057bd7bd0791fc2387a0a79b07c8e44480419c61

I implement the approved optional field selector for the real customer search function and CLI. I preserve existing two-argument calls and default name/email matching. I began from implementation parent commit `1686d0d`, after the approved baseline and run-context preparation.

## Requirements Covered

I implement FR-07 with FR-01 through FR-06 as regression obligations, and exercise NFR-01 / NFR-02 locally. I map my focused evidence as follows:

| Criteria | Tests I add |
|---|---|
| AC-11 | I compare default and explicit `all`, ordered results, single output for both-field matches, new list identity and unchanged record identity in `test_search_fields.py`; I compare default/all CLI rows in `test_cli_fields.py`. |
| AC-12 | I exercise name/email isolation, partial trimmed casefold matching, Unicode sharp-s, interior spaces, generator input and no matches in `test_search_fields.py`. |
| AC-13 | I reject unsupported, blank, differently cased, padded, non-string and unhashable selectors; I preserve blank/non-text query errors for each valid selector in `test_search_fields.py`. |
| AC-14 | I exercise options before/after the term, exact row formatting, valid no matches, blank queries, invalid choices, missing selector values and missing/excess terms through subprocesses in `test_cli_fields.py`. |
| AC-15 | I import the actual public production API and launch `python -m customer_search` in subprocesses; I retain the complete existing suite and empty runtime dependencies. |

I retain AC-01 through AC-10 in the unchanged existing tests and complete gate.

## Implementation Plan

1. I read the approved contracts, production paths, existing tests and run context, then run and retain a complete baseline.
2. I add focused tests against the production function and subprocess CLI and retain their failing results before editing production code.
3. I add a keyword-only `field="all"`, validate it in the domain and restrict matching to the selected existing field(s). I add argparse choices and pass the selector to the domain.
4. I run focused tests and the shared gate, inspect the diff and API, document usage/evidence, and create a local implementation commit for independent review.

## Files Changed

- I extend `src/customer_search/search.py` with selector validation and matching.
- I extend `src/customer_search/cli.py` with `--field` parsing and delegation.
- I add `tests/test_search_fields.py` and `tests/test_cli_fields.py` without changing existing tests.
- I add field-selector usage examples to `README.md`.
- I add this report and command evidence under `results/evidence/ada09-coder-*`.

## Tests Added / Updated

I add 44 domain test cases and 40 real CLI subprocess cases, for 84 focused cases. I retain all 60 existing cases unchanged. I use no mocks, copied matching implementation, synthetic production API or added runtime package.

## Commands Executed

I use `$PYTHON` for the explicitly selected local Python 3.13 interpreter and `<repo>` for the repository root in published evidence. I execute commands from `<repo>`.

| Command I execute | Result I retain | Evidence |
|---|---|---|
| `PYTHON=$PYTHON ./scripts/verify_repo.sh` before test additions | I obtain 60 passed; all four stages pass; exit 0. | `evidence/ada09-coder-baseline.log` and `.exitcode` |
| `$PYTHON -m pytest -q -p no:cacheprovider tests/test_search_fields.py tests/test_cli_fields.py` before production edits | I obtain 79 failed / 5 passed; exit 1. | `evidence/ada09-coder-red.log` and `.exitcode` |
| The same focused pytest command after production edits | I obtain 84 passed; exit 0. | `evidence/ada09-coder-green.log` and `.exitcode` |
| `PYTHON=$PYTHON ./scripts/verify_repo.sh` after implementation | I obtain 144 passed, Ruff PASS, contract PASS, security PASS and `VERIFY_REPO: PASS`; exit 0. | `evidence/ada09-coder-verify.log` and `.exitcode` |
| `git diff --check`, scoped `git diff --name-only`, and `$PYTHON -c` API/dependency inventory | I obtain exit 0 for each command and confirm the actual keyword-only signature and empty runtime dependencies. | `evidence/ada09-coder-inspection.log` and `.exitcode` |

I also read the local contracts, source/tests and gate with `cat` / `rg`, inspect `git status`, the implementation diff, and the existing local Git identity. I retain complete test/gate output rather than replacing failed evidence with a successful run.

## Verification Result

I observe a local functional PASS: 144 tests pass and every shared gate stage exits 0. I observe meaningful red evidence: the original function rejects the new keyword and the original CLI rejects valid new options, with 79 focused failures before implementation. I retain five preimplementation passes for already-existing TypeError/usage protections. I make no independent-review or remote-CI claim from these local results.

## Assumptions

I use the approved selector contract exactly: `all`, `name` and `email` are case-sensitive, untrimmed values. I leave precedence unspecified when both the query and selector are invalid; each invalid selector raises `ValueError`, and each valid selector retains existing query validation. I preserve the existing standard-library-only runtime and domain/CLI boundary.

## Known Limitations

I verify locally on Python 3.13; I do not assert a Python 3.11 execution or hosted CI result. I leave independent review, human finding decisions, any accepted fixes, re-review and readiness decisions to their subsequent roles. I treat the security pattern gate as bounded detection. I do not modify the inherited protected evidence or publish externally.

## Self-Check

I inspect production changes and confirm that only search.py and cli.py change. I add only the two permitted test modules and retain existing tests, models, frozen data, requirements, architecture, guardrails and runtime dependencies. I confirm the public function exists in the production package with the required keyword-only parameter and that CLI calls it directly. I observe passing protected-hash, import-boundary and whitespace checks. I leave other roles' artifacts outside my implementation commit and do not approve my own change.

## Fix Cycle

I address only the accepted RF-01 evidence clarity action recorded in `results/human-review-decisions.md`. I preserve the original patch/history at immutable base `057bd7bd0791fc2387a0a79b07c8e44480419c61` and historical head `57f464c06ec01d2e1af4b3dcf3895d5e182f4516` as `results/evidence/ada09-initial-implementation.diff` and `ada09-initial-commits.txt`.

I regenerate `results/pr.diff` and `results/commits.txt` for the complete frozen base-to-reviewed-candidate range ending at `b32491e514241cc8110c34cdd9617948b5c347c7`, without exclusions. I add `results/pr-diff-scope.json` with exact generation argv, relative artifact paths, immutable implementation/historical/reviewed boundaries and SHA-256 fingerprints. I distinguish the subsequent review/decision commits and this evidence correction from the frozen snapshot. I explain those boundaries in `results/verification-report.md` while retaining every original execution log.

I run `PYTHON=$PYTHON ./scripts/verify_repo.sh` in the original local Python environment and observe 144 passing cases, all four gate stages PASS and exit 0. I retain the new log, exit code and execution timestamps under `results/evidence/ada09-fix-*`. I compare source/test, product-contract and dependency-declaration fingerprints before/after and verify byte identity. I also verify both historical artifacts and both complete candidate artifacts against their declared immutable Git ranges and run `git diff --check`.

I change no production code, tests, requirements or dependencies for this finding and preserve other roles' reports/decisions/context files. I add no new product regression because this accepted action changes only evidence. I retain the local Python 3.13 and hosted-execution limitations above. I submit this correction for independent re-review and leave resolution status to that role.

I retain an unfiltered `git diff --check` exit 2 for six warnings inside the required verbatim nested patch in `results/pr.diff`. I preserve its exact generated bytes and matching SHA-256. I obtain exit 0 when checking editable documentation. I also retain a staged check exit 2 for those spaces reproduced in the raw diagnostic log and obtain exit 0 for the final staged editable-document check excluding only the two generated patch artifacts and that raw log. I retain these actual results and exclude nothing from complete candidate generation or boundary verification.
