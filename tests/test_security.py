"""I exercise security checks against isolated files without publishing token literals."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('security_check', ROOT / 'scripts/check_security.py')
SECURITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SECURITY)


def test_clean_project_is_accepted(tmp_path):
    (tmp_path / 'readme.md').write_text('I document a local example.\n')
    assert SECURITY.scan(tmp_path) == []


def test_embedded_credential_is_detected_without_exposing_it(tmp_path):
    secret = 'ghp_' + 'a' * 36
    (tmp_path / 'config.txt').write_text(secret)
    errors = SECURITY.scan(tmp_path)
    assert any('GitHub token' in error for error in errors)
    assert all(secret not in error for error in errors)


def test_nested_environment_file_is_detected(tmp_path):
    folder = tmp_path / 'config'
    folder.mkdir()
    (folder / '.env.local').write_text('EXAMPLE=demo\n')
    assert any('sensitive file' in error for error in SECURITY.scan(tmp_path))


def test_private_key_header_is_detected(tmp_path):
    (tmp_path / 'example.txt').write_text('-----BEGIN ' + 'PRIVATE KEY-----\nexample')
    assert any('private key pattern' in error for error in SECURITY.scan(tmp_path))


def test_symlink_is_rejected_without_reading_its_target(tmp_path):
    (tmp_path / 'link').symlink_to(tmp_path / 'missing')
    assert any('symlink not scanned' in error for error in SECURITY.scan(tmp_path))
