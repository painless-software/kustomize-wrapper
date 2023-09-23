"""
Tests for command line interface (CLI)
"""
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

import os

import pytest
from cli_test_helpers import shell

import kustomize


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = shell('python -m kustomize')
    assert result.exit_code == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = shell('kustomize --help')
    assert result.exit_code == 0


def test_apply_command():
    """
    Is command available?
    """
    result = shell('kustomize apply --help')
    assert result.exit_code == 0


def test_build_command():
    """
    Is command available?
    """
    result = shell('kustomize build --help')
    assert result.exit_code == 0


def test_lint_command():
    """
    Is command available?
    """
    result = shell('kustomize lint --help')
    assert result.exit_code == 0


def test_lint_fail_fast_option():
    """
    Does command provide the specific option?
    """
    result = shell('kustomize lint --fail-fast --help')
    assert result.exit_code == 0


def test_lint_force_color_option():
    """
    Does command provide the specific option?
    """
    result = shell('kustomize lint --force-color --help')
    assert result.exit_code == 0


def test_lint_ignore_missing_schemas_option():
    """
    Does command provide the specific option?
    """
    result = shell('kustomize lint --ignore-missing-schemas --help')
    assert result.exit_code == 0


def test_version_option():
    """
    Does --version yield a proper value?
    """
    package_version = metadata.version("kustomize_wrapper")
    expected_output = f"kustomize, version {package_version}{os.linesep}"

    result = shell('kustomize --version')
    assert result.stdout == expected_output
    assert result.exit_code == 0


def test_version_command():
    """
    Is command available?
    """
    result = shell('kustomize version --help')
    assert result.exit_code == 0


def test_version_update_option():
    """
    Does command provide the specific option?
    """
    result = shell('kustomize version --update --help')
    assert result.exit_code == 0


def test_cli():
    """
    Does CLI stop execution w/o a command argument?
    """
    with pytest.raises(SystemExit):
        kustomize.cli.main()
