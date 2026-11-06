# Customer Search Specification

## Goal and Requirements Covered

I locate existing customer records from a local CLI with one term. I cover FR-01 through FR-07 and NFR-01 through NFR-03 from `REQUIREMENTS.md`.

## Scope

I query a fixed in-memory collection of fictional customers. I exclude creation, updates, deletion, persistence, HTTP endpoints, pagination, ranking and searches of other fields.

## Domain Model

I represent a customer with `Customer(id, name, email)`. I require `id` to be non-empty text; I preserve valid text verbatim, including whitespace, without trimming or new format rules. I reject a non-string or empty-string identifier at construction with `ValueError`. I leave name and email validation unchanged. I preserve frozen instances and read-only demo data.

I clarified the existing non-empty textual ID rule for CR-ADA08-01 before the baseline tag and either controlled run; I did not add it after seeing a failing implementation. I keep the archived original specification unchanged.

## Search Rules

I strip outer query whitespace, apply `str.casefold()` to the query and both searchable fields, and use substring membership in either name or email. I return each matching input record once even when both fields match. I preserve input order and interior query spaces. I accept any `Iterable[Customer]` and return a new list. I do not add accent normalization or fuzzy matching.

## Field Selection

I extend the function with the keyword-only parameter `field: str = "all"`. I accept exactly `all`, `name` and `email`, case-sensitively. I apply the existing term trimming and Unicode casefold rules to the selected field(s). I preserve ordering, interior query spaces, single-pass iterable support and one output per matching input record. I keep existing two-argument callers valid. I do not normalize, trim or silently coerce the selector.

I expose the option as `--field {all,name,email}` in the CLI, with `all` as the default. I keep exactly one positional term and permit the option before or after it. I reject invalid selectors at the domain boundary with `ValueError`, including non-string and unhashable values; the CLI reports a usage/error message on stderr, no result rows on stdout, and exit 2. I preserve existing valid/no-match output and exit codes.

## Validation Rules

I require a textual query with at least one character after outer trimming. I require exactly one positional CLI argument. I distinguish query normalization from identifier preservation.

## Error Handling

I raise `ValueError` for invalid query input and invalid customer identifiers. I translate query errors to a useful Spanish message on stderr and CLI exit 2. I let argparse report missing or excess arguments with exit 2. I print `No se encontraron clientes.` with exit 0 for valid queries without matches. I print identifier, name and email for matches and return exit 0.

## Acceptance Criteria

- **AC-01 (FR-01):** I find customers by a term in either name or email.
- **AC-02 (FR-02):** I find a customer with a partial field fragment.
- **AC-03 (FR-03):** I retain matches when query casing changes, including Unicode casefold cases.
- **AC-04 (FR-04):** I show identifier, name and email in each CLI result.
- **AC-05 (FR-05):** I show the specified no-match message and exit 0.
- **AC-06 (FR-06):** I reject blank queries with a useful error and CLI exit 2.
- **AC-07 (NFR-01):** I execute automated acceptance tests with pytest, including input order and no duplicated output from matching both fields.
- **AC-08 (NFR-02):** I search without network, credentials or nonstandard runtime packages.
- **AC-09 (NFR-03):** I document Python, installation, run and test commands in README.
- **AC-10 (FR-04):** I reject non-text or empty identifiers at construction, preserve every non-empty textual identifier and keep customers immutable.
- **AC-11 (FR-01, FR-07):** I preserve default and explicit `all` results, ordering, no duplicate output from matching both fields, and the existing two-argument API.
- **AC-12 (FR-02, FR-03, FR-07):** I restrict matches to the selected `name` or `email` field and retain partial, trimmed, casefold matching, interior spaces and generator support.
- **AC-13 (FR-06, FR-07):** I reject unsupported, blank, differently cased and non-string field selectors with `ValueError`, including unhashable inputs. I retain invalid-query behavior for every valid selector.
- **AC-14 (FR-04, FR-05, FR-07):** I accept `--field` before or after the positional term, preserve result formatting, return exit 0 for valid no-match queries and exit 2 with stderr/no result stdout for invalid selectors or missing selector values.
- **AC-15 (NFR-01, NFR-02, FR-07):** I verify the real production function and CLI through tests without fabricating APIs, adding runtime dependencies or bypassing the domain validation layer.

## Test Scenarios

I exercise name/email fragments, both-field matching, casing, Unicode sharp-s, order, generators, interior/outer spaces, absent records, blank and non-text queries, missing/extra CLI arguments, output fields and exit codes. I exercise invalid IDs, valid ID preservation and frozen-instance behavior for CR-ADA08-01.

## Constraints and Open Questions

I apply the constraints in `REQUIREMENTS.md`. I retain the resolved Q-01/Q-02 decisions there and introduce no unresolved product question in this task.
