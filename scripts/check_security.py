#!/usr/bin/env python3
"""I detect known credential patterns and sensitive files without displaying contents."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '.venv', 'work', 'outputs', '__pycache__', '.pytest_cache', '.ruff_cache'}
PATTERNS = (
    ('GitHub token', re.compile(rb'gh[pousr]_[A-Za-z0-9]{20,}')),
    ('GitHub fine-grained token', re.compile(rb'github_pat_[A-Za-z0-9_]{20,}')),
    ('private key', re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
    ('AWS access key', re.compile(rb'AKIA[0-9A-Z]{16}')),
    ('OpenAI project key', re.compile(rb'sk-proj-[A-Za-z0-9_-]{20,}')),
)


def scan(root: Path) -> list[str]:
    errors = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in IGNORED or part.endswith('.egg-info') for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f'symlink not scanned: {relative}')
            continue
        if not path.is_file():
            continue
        if path.name == '.env' or path.name.startswith('.env.') or path.name in {'id_rsa', 'id_ed25519', 'credentials.json'}:
            errors.append(f'sensitive file: {relative}')
        try:
            data = path.read_bytes()
        except OSError:
            errors.append(f'unreadable file: {relative}')
            continue
        for label, pattern in PATTERNS:
            if pattern.search(data):
                errors.append(f'{label} pattern: {relative}')
    return errors


def main():
    errors = scan(ROOT)
    if errors:
        for error in errors:
            print('SECURITY: FAIL: ' + error, file=sys.stderr)
        return 1
    print('SECURITY: PASS (known patterns, sensitive filenames, symlinks)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
