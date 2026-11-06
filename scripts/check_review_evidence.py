#!/usr/bin/env python3
"""I validate the recorded review cycle without replacing human judgment."""

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'CHANGE_REQUEST.md', 'AI_USAGE_LOG.md', 'results/run-context.md',
    'results/coder-report.md', 'results/verification-report.md', 'results/pr.diff',
    'results/commits.txt', 'results/review-contract.md', 'results/review-report.md',
    'results/human-review-decisions.md', 'results/re-review-report.md', 'results/PR_EVIDENCE.md',
)


def validate(ledger: dict, final: bool) -> list[str]:
    errors = []
    if ledger.get('change_id') != 'CR-ADA09-01':
        errors.append('unknown change identifier')
    for key in ('base_commit', 'candidate_commit', 'final_code_commit'):
        if not re.fullmatch(r'[0-9a-f]{40}', ledger.get(key, '')):
            errors.append('missing immutable commit: ' + key)
    if not ledger.get('coder_context') or not ledger.get('reviewer_context'):
        errors.append('coder and reviewer context identifiers are required')
    elif ledger['coder_context'] == ledger['reviewer_context']:
        errors.append('coder and reviewer must have independent contexts')
    if ledger.get('source_unchanged_during_review') is not True:
        errors.append('read-only review integrity is not demonstrated')
    if ledger.get('gate') != 'PASS':
        errors.append('verification gate is not PASS')
    findings = ledger.get('findings', [])
    if not isinstance(findings, list):
        return errors + ['findings must be a list']
    ids = []
    for finding in findings:
        identifier = finding.get('id', '')
        ids.append(identifier)
        if not re.fullmatch(r'RF-\d{2,}', identifier):
            errors.append('invalid finding identifier')
        if finding.get('severity') not in {'MUST FIX', 'SHOULD FIX', 'OPTIONAL'}:
            errors.append(identifier + ': invalid severity')
        for key in ('requirement', 'file', 'evidence', 'risk', 'recommendation'):
            if not finding.get(key):
                errors.append(identifier + ': missing ' + key)
        if not isinstance(finding.get('line'), int) or finding.get('line', 0) < 1:
            errors.append(identifier + ': a concrete line is required')
        if final:
            decision = finding.get('decision')
            if decision not in {'ACCEPTED', 'REJECTED', 'MODIFIED', 'DEFERRED'} or not finding.get('human_reason'):
                errors.append(identifier + ': missing human decision/rationale')
            if decision in {'ACCEPTED', 'MODIFIED'} and finding.get('resolution') != 'RESOLVED':
                errors.append(identifier + ': accepted/modified finding is unresolved')
            if decision == 'DEFERRED' and finding.get('severity') == 'MUST FIX':
                errors.append(identifier + ': blocking finding cannot be deferred as ready')
    if len(set(ids)) != len(ids):
        errors.append('finding identifiers must be unique')
    if final:
        if ledger.get('human_decisions_approved') is not True:
            errors.append('human finding decisions are pending')
        if ledger.get('final_human_approval') is not True or not ledger.get('approved_by') or not ledger.get('approved_date'):
            errors.append('final human readiness decision is pending')
        if not ledger.get('rereviewer_context') or ledger['rereviewer_context'] == ledger.get('coder_context'):
            errors.append('independent re-review is missing')
        if ledger.get('new_must_fix') != 0:
            errors.append('new blocking findings remain')
        if ledger.get('reviewer_recommendation') != 'READY FOR HUMAN REVIEW':
            errors.append('independent reviewer has not recommended readiness')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['candidate', 'final'], default='candidate')
    args = parser.parse_args()
    errors = []
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or not path.read_text(encoding='utf-8').strip():
            errors.append('missing or empty evidence: ' + relative)
    try:
        ledger = json.loads((ROOT / 'results/review-ledger.json').read_text())
        errors.extend(validate(ledger, args.phase == 'final'))
    except (OSError, ValueError, TypeError):
        errors.append('missing or invalid structured review ledger')
    if errors:
        print('\n'.join('REVIEW EVIDENCE: FAIL: ' + error for error in errors), file=sys.stderr)
        return 1
    print('REVIEW EVIDENCE: PASS (' + args.phase + ')')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
