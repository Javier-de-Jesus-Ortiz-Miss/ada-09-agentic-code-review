# Change Request

Change ID: CR-ADA09-01

## Goal

I add an optional selector for existing customer name/email search while preserving the default behavior and public API compatibility.

## Requirements Covered

I reference FR-01 through FR-07 and NFR-01 / NFR-02 in `REQUIREMENTS.md`; I select AC-11 through AC-15 in `SPEC.md` and retain AC-01 through AC-10 as regression obligations. I leave the normative behavior in those files.

## Constraints

I follow `AGENTS.md` and preserve architecture boundaries. I limit production edits to search.py and cli.py, add focused real-production tests, retain existing tests and frozen data, and introduce no runtime dependency. I keep implementation and independent review in separate agent contexts.

## Implementation Plan

I first inspect the approved requirements and existing production code/tests. I add focused domain and subprocess CLI regressions, then implement domain field validation/matching and CLI argument delegation. I run the shared gate, inspect the diff and produce the coder report. I pass the committed candidate to a separate read-only reviewer.

## Verification

I retain baseline and candidate commits, relevant failing/passing regressions, the complete gate output and exit code, an inspectable diff and an API existence inventory. I require independent findings, actual human decisions, re-review status and a consolidated PR evidence report.

## Human Approval

Approved to implement: YES
Approved by: Javier Ortiz
Date: 2026-11-05
Plan approved: YES
