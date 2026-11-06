"""I exercise the real CLI subprocess for AC-14 and AC-15."""

import os
from pathlib import Path
import subprocess
import sys

import pytest


def run_cli(*arguments):
    env = os.environ.copy()
    src = str(Path(__file__).resolve().parents[1] / "src")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [src, env.get("PYTHONPATH")]))
    return subprocess.run(
        [sys.executable, "-m", "customer_search", *arguments],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("before_term", [True, False])
@pytest.mark.parametrize(
    ("field", "term", "expected"),
    [
        ("all", "  ANA  ", "C001 | Ana López | ana.lopez@example.com\n"),
        ("name", "  LÓPEZ  ", "C001 | Ana López | ana.lopez@example.com\n"),
        ("email", "  ANA.LOPEZ  ", "C001 | Ana López | ana.lopez@example.com\n"),
        ("name", "example.com", "No se encontraron clientes.\n"),
        ("email", "López", "No se encontraron clientes.\n"),
    ],
)
def test_cli_field_before_or_after_term_preserves_formatting(before_term, field, term, expected):
    arguments = ("--field", field, term) if before_term else (term, "--field", field)
    result = run_cli(*arguments)
    assert result.returncode == 0
    assert result.stdout == expected
    assert result.stderr == ""


def test_cli_default_and_all_have_identical_ordered_results():
    default = run_cli("example.com")
    explicit = run_cli("example.com", "--field", "all")
    assert default.returncode == explicit.returncode == 0
    assert default.stdout == explicit.stdout
    assert default.stderr == explicit.stderr == ""
    assert [line.split(" | ")[0] for line in explicit.stdout.splitlines()] == [
        "C001", "C002", "C003", "C004"
    ]


@pytest.mark.parametrize("field", ["all", "name", "email"])
def test_cli_selected_field_no_matches(field):
    result = run_cli("absent", "--field", field)
    assert result.returncode == 0
    assert result.stdout == "No se encontraron clientes.\n"
    assert result.stderr == ""


@pytest.mark.parametrize("field", ["all", "name", "email"])
@pytest.mark.parametrize("term", ["", " \t\n"])
def test_cli_selected_field_retains_blank_query_errors(field, term):
    result = run_cli(term, "--field", field)
    assert result.returncode == 2
    assert "Error:" in result.stderr
    assert "no vacío" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("field", ["id", "Name", "ALL", "EMAIL", "", " ", " name", "email "])
@pytest.mark.parametrize("before_term", [True, False])
def test_cli_rejects_invalid_selector_with_usage_only(field, before_term):
    arguments = ("--field", field, "ana") if before_term else ("ana", "--field", field)
    result = run_cli(*arguments)
    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert "invalid choice" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize(
    "arguments",
    [("ana", "--field"), ("--field",), ("--field", "name"),
     ("--field", "email", "ana", "bruno")],
)
def test_cli_rejects_missing_field_value_or_wrong_term_count(arguments):
    result = run_cli(*arguments)
    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert result.stdout == ""
