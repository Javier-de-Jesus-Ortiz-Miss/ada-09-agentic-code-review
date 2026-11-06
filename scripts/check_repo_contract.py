#!/usr/bin/env python3
"""I validate repository contracts and protected artifacts without mutating them."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]
ESSENTIAL = (
    'CHANGE_REQUEST.md', 'docs/REVIEW_RULES.md', 'scripts/check_security.py',
    'scripts/check_review_evidence.py',
    'AGENTS.md', 'README.md', 'REQUIREMENTS.md', 'SPEC.md', 'ARCHITECTURE.md',
    'TASKS.md', 'TASK_UNDER_TEST.md', 'REPOSITORY_READINESS_AUDIT.md', 'AI_USAGE_LOG.md',
    'docs/REPO_MAP.md', 'docs/EXPERIMENT.md', 'docs/traceability.md',
    'docs/protected-paths.json', 'docs/EXPERIMENT_PROMPT.txt',
    'scripts/verify_repo.sh', 'scripts/check_repo_contract.py',
    'scripts/package_delivery.py', '.github/workflows/verify.yml',
    'pyproject.toml', 'requirements-dev.txt',
    'src/customer_search/models.py', 'src/customer_search/search.py',
    'src/customer_search/data.py', 'src/customer_search/cli.py',
    'tests/test_search.py', 'tests/test_cli.py', 'tests/test_repo_contract.py',
    'results/before-agent-run.md', 'results/after-agent-run.md',
    'results/readiness-improvement-report.md', 'results/implicit-knowledge.md',
    'results/evidence/source-provenance.json', 'results/evidence/audit-before.json',
    'results/evidence/functional-baseline.json',
)
# I intentionally do not require test_model_validation.py before the controlled change.
HEADINGS = {
    'AGENTS.md': ('Read First', 'Sources of Truth', 'Repository Map', 'Standard Commands',
                  'Change Rules', 'Safety and Permissions', 'Stop Conditions', 'Definition of Done'),
    'docs/REPO_MAP.md': ('Entry Points', 'Tests', 'Change Guide', 'Do Not Edit Directly'),
    'TASK_UNDER_TEST.md': ('Goal', 'Requirements Covered', 'Verification', 'Constraints'),
    'results/before-agent-run.md': ('Run Context', 'Clarification Questions', 'Repository Exploration',
                                   'Incorrect Assumptions', 'Failed / Unknown Commands',
                                   'Out-of-Scope Changes', 'Validation Evidence', 'Final Result'),
    'results/after-agent-run.md': ('Run Context', 'Clarification Questions', 'Repository Exploration',
                                  'Incorrect Assumptions', 'Failed / Unknown Commands',
                                  'Out-of-Scope Changes', 'Validation Evidence', 'Final Result'),
}
FIXED_PROTECTED = {
    'src/customer_search/data.py', 'TASK_UNDER_TEST.md', 'docs/EXPERIMENT_PROMPT.txt',
    'results/evidence/source-provenance.json', 'results/evidence/audit-before.json',
    'results/evidence/functional-baseline.json',
}
ALLOWED_LOCAL = {
    'models': set(), 'data': {'models'}, 'search': {'models'},
    'cli': {'data', 'search'}, '__main__': {'cli'}, '__init__': {'models', 'search'},
}


def visible_markdown(text: str) -> str:
    """I exclude fenced examples and comments from heading/reference validation."""
    text = re.sub(r'<!--.*?(?:-->|\Z)', '', text, flags=re.S)
    lines = []
    fence = None
    width = 0
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is None:
            if match:
                fence, width = match[1][0], len(match[1])
            else:
                lines.append(line)
        elif match and match[1][0] == fence and len(match[1]) >= width and not match[2].strip():
            fence = None
    return '\n'.join(lines)


def protected_paths(root: Path) -> set[str]:
    paths = set(FIXED_PROTECTED)
    for folder in ('results/prior', 'skills'):
        paths.update(str(p.relative_to(root)) for p in (root / folder).rglob('*') if p.is_file())
    return paths


def check(root: Path) -> list[str]:
    errors: list[str] = []
    text: dict[str, str] = {}
    for rel in ESSENTIAL:
        path = root / rel
        # I check every ancestor to prevent a directory symlink from redirecting a contract.
        chain = [root.joinpath(*Path(rel).parts[:i]) for i in range(1, len(Path(rel).parts) + 1)]
        if any(p.is_symlink() for p in chain):
            errors.append(f'symlink is forbidden for essential path: {rel}')
        if not path.is_file():
            errors.append(f'missing essential file: {rel}')
            continue
        try:
            content = path.read_text(encoding='utf-8')
            if not content.strip():
                errors.append(f'empty essential file: {rel}')
            text[rel] = content
        except (OSError, UnicodeError) as exc:
            errors.append(f'unreadable essential file: {rel}: {exc.__class__.__name__}')

    for rel, headings in HEADINGS.items():
        content = visible_markdown(text.get(rel, ''))
        found = re.findall(r'^## (.+?)\s*$', content, re.M)
        for heading in headings:
            if found.count(heading) != 1:
                errors.append(f'required unique heading missing/duplicated: {rel}: {heading}')
            else:
                body = re.split(r'^## ', content, flags=re.M)[found.index(heading) + 1]
                if not body.partition('\n')[2].strip():
                    errors.append(f'empty contract section: {rel}: {heading}')

    for rel in ('AGENTS.md', 'docs/REPO_MAP.md'):
        for source in ('REQUIREMENTS.md', 'SPEC.md', 'ARCHITECTURE.md', 'TASKS.md'):
            if source not in visible_markdown(text.get(rel, '')):
                errors.append(f'missing source-of-truth reference: {rel}: {source}')
    for rel in ('README.md', 'docs/REPO_MAP.md'):
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', visible_markdown(text.get(rel, ''))):
            if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                continue
            path = ((root / rel).parent / target.split('#')[0]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append(f'broken or escaping local link: {rel}: {target}')

    task = visible_markdown(text.get('TASK_UNDER_TEST.md', ''))
    if len(re.findall(r'^Change ID: CR-[A-Z0-9-]+\s*$', task, re.M)) != 1:
        errors.append('task must have one explicit Change ID')
    for prefix, source in (('FR', 'REQUIREMENTS.md'), ('AC', 'SPEC.md')):
        known = set(re.findall(r'\b' + prefix + r'-\d{2}\b', text.get(source, '')))
        references = set(re.findall(r'\b' + prefix + r'-\d{2}\b', task))
        if not references or not references <= known:
            errors.append(f'task has missing or unresolved {prefix} references')

    try:
        manifest = json.loads(text.get('docs/protected-paths.json', '{}'))
        expected = protected_paths(root)
        entries = manifest.get('files', {})
        if manifest.get('schema_version') != 1 or set(entries) != expected:
            errors.append('protected manifest must cover exactly all declared protected paths')
        for rel, digest in sorted(entries.items()):
            path = root / rel
            ancestors = [root.joinpath(*Path(rel).parts[:i]) for i in range(1, len(Path(rel).parts) + 1)]
            if Path(rel).is_absolute() or '..' in Path(rel).parts or any(p.is_symlink() for p in ancestors):
                errors.append(f'unsafe protected path: {rel}')
            elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f'protected file changed or missing: {rel}')
    except (OSError, ValueError, TypeError, AttributeError):
        errors.append('invalid protected manifest')

    for rel in ('.env', 'id_rsa', 'id_ed25519', 'credentials.json'):
        if os.path.lexists(root / rel):
            errors.append(f'forbidden sensitive root path: {rel}')
    for path in (root / 'src').rglob('*'):
        if path.is_symlink():
            errors.append(f'symlink in source: {path.relative_to(root)}')

    try:
        config = tomllib.loads(text.get('pyproject.toml', ''))
        if config.get('project', {}).get('dependencies') != []:
            errors.append('runtime dependencies must remain empty')
        if config.get('tool', {}).get('pytest', {}).get('ini_options', {}).get('testpaths') != ['tests']:
            errors.append('pytest must target active tests only')
    except (ValueError, TypeError):
        errors.append('invalid pyproject.toml')

    for module, allowed in ALLOWED_LOCAL.items():
        path = root / 'src/customer_search' / f'{module}.py'
        try:
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        if node.level != 1 or not node.module or node.module.split('.')[0] not in allowed:
                            errors.append(f'architecture dependency violation: {module}: relative import')
                    elif node.module:
                        names = [node.module]
                for name in names:
                    base = name.split('.')[0]
                    if base == 'customer_search':
                        local = name.split('.')[1] if '.' in name else None
                        if local not in allowed:
                            errors.append(f'architecture dependency violation: {module}: {name}')
                    elif base not in sys.stdlib_module_names:
                        errors.append(f'nonstandard runtime import: {module}: {name}')
                if module in {'models', 'search'}:
                    if names and any(n.split('.')[0] in {'os', 'sys', 'pathlib', 'subprocess', 'socket', 'urllib', 'http', 'io'} for n in names):
                        errors.append(f'domain I/O dependency violation: {module}')
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'print', 'open', 'input', 'exec', 'eval', '__import__'}:
                        errors.append(f'domain side-effect call: {module}: {node.func.id}')
        except (OSError, SyntaxError, UnicodeError):
            errors.append(f'unreadable or invalid runtime module: {module}')

    try:
        workflow = yaml.load(text.get('.github/workflows/verify.yml', ''), Loader=yaml.BaseLoader)
        if workflow['permissions'] != {'contents': 'read'}:
            errors.append('CI permissions must be contents: read only')
        if not {'push', 'pull_request'} <= set(workflow['on']):
            errors.append('CI must independently run on push and pull_request')
        steps = workflow['jobs']['verify']['steps']
        if not any(s.get('run') == './scripts/verify_repo.sh' for s in steps):
            errors.append('CI must invoke the single shared verification script')
        if any(re.search(r'\bpytest\b|\bruff check\b|check_repo_contract\.py', s.get('run', '')) for s in steps):
            errors.append('CI must not duplicate gate stage logic')
    except (KeyError, TypeError, AttributeError, yaml.YAMLError):
        errors.append('invalid CI workflow structure')

    verify = text.get('scripts/verify_repo.sh', '')
    for required in ('set -euo pipefail', '-m pytest', '-m ruff check', 'scripts/check_repo_contract.py'):
        if required not in verify:
            errors.append(f'verification script missing stage/safety marker: {required}')
    script = root / 'scripts/verify_repo.sh'
    if script.is_file() and not script.stat().st_mode & stat.S_IXUSR:
        errors.append('verification script must be executable')
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = check(args.root.resolve())
    if errors:
        for error in errors:
            print(f'CONTRACT: FAIL: {error}', file=sys.stderr)
        return 1
    print('CONTRACT: PASS (files, headings, references, protected hashes, boundaries, CI)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
