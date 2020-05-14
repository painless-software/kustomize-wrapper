"""
Tests for the lint command module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import patch

import kustomize


@patch('kustomize.commands.lint.lint')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'lint', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('builtins.print')
def test_fail_fast(mock_print):
    """
    Is the correct code called when invoked with option?
    """
    with ArgvContext('kustomize', 'lint', '--fail-fast', 'folder'), \
            pytest.raises(SystemExit):
        kustomize.cli.main()

    assert str(mock_print.call_args).startswith(
        "call('Validation of your manifests FAILED.'")


@patch('kustomize.commands.lint.shell')
def test_uses_shell(mock_shell):
    """
    Does command use the shell function to run commands?
    """
    with pytest.raises(SystemExit):
        kustomize.commands.lint.lint(['foo', 'bar', 'baz'],
                                     edit=None,
                                     fail_fast=False,
                                     force_color=False,
                                     ignore_missing_schemas=False)

    assert mock_shell.call_count == 3, \
        "Should call shell() function 3 times"
