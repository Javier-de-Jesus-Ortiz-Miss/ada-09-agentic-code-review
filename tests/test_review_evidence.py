"""I verify that evidence checks cannot equate green tests with human approval."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('review_evidence', ROOT / 'scripts/check_review_evidence.py')
EVIDENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVIDENCE)


def complete_ledger():
    return {
        'change_id': 'CR-ADA09-01', 'base_commit': 'a' * 40,
        'candidate_commit': 'b' * 40, 'final_code_commit': 'c' * 40,
        'coder_context': 'coder-1', 'reviewer_context': 'reviewer-1',
        'rereviewer_context': 'reviewer-2', 'source_unchanged_during_review': True,
        'gate': 'PASS', 'findings': [], 'human_decisions_approved': True,
        'final_human_approval': True, 'approved_by': 'Javier Ortiz',
        'approved_date': '2026-11-05', 'new_must_fix': 0,
        'reviewer_recommendation': 'READY FOR HUMAN REVIEW',
    }


def test_complete_structured_evidence_is_accepted():
    assert EVIDENCE.validate(complete_ledger(), True) == []


def test_shared_coder_reviewer_context_is_rejected():
    ledger = complete_ledger()
    ledger['reviewer_context'] = ledger['coder_context']
    assert any('independent contexts' in e for e in EVIDENCE.validate(ledger, True))


def test_green_gate_does_not_replace_human_readiness_decision():
    ledger = complete_ledger()
    ledger['final_human_approval'] = False
    assert any('final human readiness' in e for e in EVIDENCE.validate(ledger, True))


def test_finding_without_concrete_evidence_is_rejected():
    ledger = complete_ledger()
    ledger['findings'] = [{'id': 'RF-01', 'severity': 'MUST FIX'}]
    assert any('missing evidence' in e for e in EVIDENCE.validate(ledger, False))


def test_accepted_blocker_must_be_resolved():
    ledger = complete_ledger()
    ledger['findings'] = [{
        'id': 'RF-01', 'severity': 'MUST FIX', 'requirement': 'AC-13',
        'file': 'src/customer_search/search.py', 'line': 1, 'evidence': 'Observed failure',
        'risk': 'Invalid input leaks an exception', 'recommendation': 'Validate the selector',
        'decision': 'ACCEPTED', 'human_reason': 'I confirmed the specified behavior.',
        'resolution': 'NOT RESOLVED',
    }]
    assert any('unresolved' in e for e in EVIDENCE.validate(ledger, True))
