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


@patch('kustomize.commands.lint.shell')
def test_uses_shell(mock_shell):
    """
    Does command use the shell function to run commands?
    """
    kustomize.commands.lint.lint(folders=['foo', 'bar'], edit=None)

    assert mock_shell.called, "Doesn't use shell() function"
