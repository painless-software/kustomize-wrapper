"""
Tests for command line interface (CLI)
"""
import os
import pytest

import kustomize.cli


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    exit_status = os.system('python -m kustomize')
    assert exit_status == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system('kustomize --help')
    assert exit_status == 0


def test_apply_command():
    """
    Is command available?
    """
    exit_status = os.system('kustomize apply --help')
    assert exit_status == 0


def test_lint_command():
    """
    Is command available?
    """
    exit_status = os.system('kustomize lint --help')
    assert exit_status == 0


def test_version_command():
    """
    Is command available?
    """
    exit_status = os.system('kustomize version --help')
    assert exit_status == 0


def test_cli():
    """
    Does CLI stop execution w/o a command argument?
    """
    with pytest.raises(SystemExit):
        kustomize.cli.main()
        pytest.fail("CLI doesn't abort asking for a command argument")
