# Independent Review Contract

## Review Context

I act as the first independent reviewer in fresh agent context `/root/ada09_reviewer`. I received repository location, immutable commit identifiers and review instructions, without coder conversation history. I recorded this contract before opening any candidate diff.

I review CR-ADA09-01 from base `057bd7bd0791fc2387a0a79b07c8e44480419c61` to candidate `b32491e514241cc8110c34cdd9617948b5c347c7`; I use implementation commit `a551970a7f80b0aa5e9a0302a6b0718d66dd88ee` only to interpret verification provenance. I treat these identifiers as inputs to verify, rather than evidence of correctness.

## Requirements and Authority

I read CHANGE_REQUEST.md, REQUIREMENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md, TASK_UNDER_TEST.md, docs/REPO_MAP.md, AGENTS.md and docs/REVIEW_RULES.md before evaluating implementation. I use FR-07 and AC-11 through AC-15 for field selection and retain AC-01 through AC-10 as regression obligations. I treat the older ADA-08 task as historical, as the active repository contract explicitly directs.

I expect a keyword-only `field: str = "all"` in the real search function; exact case-sensitive selectors `all`, `name`, `email`; ValueError for invalid selectors including unhashable inputs; preserved two-argument behavior, query validation, Unicode casefold, substring matching, input order, single-pass iterables, interior spaces and one result per matching input record. I expect CLI parsing before or after its one positional term, preserved output, and stderr/exit 2 without result stdout for invalid selectors or missing option values.

I expect selector rules in search.py and only parsing, delegation and formatting in cli.py, with standard-library-only runtime dependencies, immutable customer/data behavior and existing tests retained.

## Review Method

I will compare the complete actual Git diff against results/pr.diff, inspect real source and tests, verify all called APIs and imports against production or the standard library, read coder/verification evidence, and execute the shared gate and independent boundary probes. I will examine test doubles, missing AC boundaries, architecture, compatibility, security and maintainability independently of green test status.

I will hash active source/tests before and after review and preserve normalized local command evidence. I may write only this contract, results/review-report.md and new results/evidence/ada09-reviewer-* artifacts. I will not edit implementation, tests, contracts, prior evidence, commits or refs, and will not delegate, publish, comment, approve or merge.

## Reporting Contract

I will include Review Context, Requirements Reviewed, Verification Evidence Reviewed, Findings, Missing Evidence / Open Questions, Summary and Reviewer Recommendation. I will classify actual findings as MUST FIX, SHOULD FIX or OPTIONAL, each with unique RF-ID, requirement/AC, concrete file/line, observed evidence, problem, risk and recommended next step. I will report None for empty categories, include an API existence table and source/test integrity confirmation, and separate technical implementation defects from evidence documentation issues.

I will recommend only NOT READY, READY AFTER MUST FIX or READY FOR HUMAN REVIEW. I will leave human approval and final readiness decisions to the human.
