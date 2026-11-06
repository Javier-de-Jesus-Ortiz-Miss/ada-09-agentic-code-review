# Architecture

## Overview

I use a local Python CLI over in-memory records. I keep argument handling, domain validation, matching and demo data separate.

## Components

| Path | Responsibility I assign | Dependencies I allow |
|---|---|---|
| `src/customer_search/models.py` | I enforce the immutable record and identifier invariant. | I allow the standard library only. |
| `src/customer_search/data.py` | I hold four fictional, read-only records. | I allow models only. |
| `src/customer_search/search.py` | I validate queries and return matches without I/O. | I allow models and the standard library. |
| `src/customer_search/cli.py` | I parse arguments, translate errors and format output. | I allow data and search. |
| `src/customer_search/__main__.py` | I start the CLI. | I allow cli. |
| `src/customer_search/__init__.py` | I expose Customer and search_customers. | I allow models and search. |

## Data Flow and Interfaces

I pass the CLI term to `search_customers(term: str, customers: Iterable[Customer], *, field: str = "all") -> list[Customer]`. I construct `Customer` before search and reject an invalid identifier in its `__post_init__` method. I return a new result list in source order, then format it in the CLI.

## Boundaries

I do not import CLI or data modules into matching or model code. I do not add printing, process execution, filesystem or network operations to the domain. I check import boundaries and direct print/open calls in `scripts/check_repo_contract.py`; I treat that AST gate as detection of declared direct imports, not a sandbox against arbitrary dynamic Python. I keep runtime dependencies empty.

## Verification and Decisions

I verify domain and CLI behavior with pytest. I use Ruff for lint and my contract checker for file presence, references, protected hashes, CI wiring and direct dependencies. I keep the linear search because the dataset is small and the feature excludes ranking/indexing. I use `casefold()` for case independence, frozen dataclasses for immutability and injected iterables for testability.

## Operational Boundaries

I keep baseline and historical evidence immutable under `docs/protected-paths.json`. I exclude the local `.venv/`, `work/` trees and delivery `outputs/` from source history. I reserve destructive operations, product requirement changes and external writes for explicit human decisions under `AGENTS.md`.

## Field Selection Boundary

I implement selector validation and matching in search.py. I limit cli.py to argument parsing, delegation and output; I do not duplicate field-matching business rules in CLI. I preserve CLI -> search -> models and CLI -> data -> models. I retain standard-library-only runtime imports and backward compatibility for existing callers.
