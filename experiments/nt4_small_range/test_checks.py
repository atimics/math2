"""Finite arithmetic and failure-detection checks; not an analytic proof."""

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


def checker():
    # A missing checker is an explicit failing specification, not an import error.
    assert importlib.util.find_spec("experiments.nt4_small_range.checks") is not None
    from experiments.nt4_small_range import checks

    return checks


def test_full_indicator_domain():
    checks = checker()
    assert checks.verify_indicator(checks.character_indicator, 256) == 32896


@pytest.mark.parametrize(
    ("order", "exponent", "expected"),
    [(1, 0, 1), (2, 0, 0), (2, 1, 1), (12, 5, 1), (12, 6, 0)],
)
def test_indicator_boundary_and_composite_orders(order, exponent, expected):
    assert checker().character_indicator(order, exponent) == Fraction(expected)


@pytest.mark.parametrize("wrong", [lambda n, k: Fraction(1), lambda n, k: Fraction(0)])
def test_checker_rejects_constant_indicators(wrong):
    with pytest.raises(AssertionError, match="indicator"):
        checker().verify_indicator(wrong, 4)


def test_exact_central_binomial_relations():
    assert checker().verify_binomial(256) == 256


def test_run_records_successful_negative_controls():
    result = checker().run()
    assert result["indicator_cases"] == 32896
    assert result["binomial_cases"] == 256
    assert len(result["negative_controls"]) == 3
    assert all(control["rejected"] for control in result["negative_controls"])
    assert result["analytic_theorem_verified_by_computation"] is False


def test_negative_control_fails_closed_when_mutation_is_not_detected():
    with pytest.raises(AssertionError, match="negative control"):
        checker().expect_rejection(lambda: None)


def test_cli_matches_checked_in_result_even_with_optimization():
    expected_path = Path(__file__).with_name("checks.json")
    assert expected_path.exists(), "checked-in result is part of the evidence packet"
    expected = json.loads(expected_path.read_text())
    completed = subprocess.run(
        [sys.executable, "-O", "-m", "experiments.nt4_small_range.checks"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(completed.stdout) == expected


def test_failure_detection_is_not_disabled_by_python_optimization():
    checker()
    completed = subprocess.run(
        [sys.executable, "-O", "-c",
         "from experiments.nt4_small_range.checks import verify_indicator; "
         "verify_indicator(lambda n, k: 1, 2)"],
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "AssertionError" in completed.stderr
