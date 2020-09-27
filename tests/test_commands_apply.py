"""
Tests for the apply command module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import call, patch

import kustomize


@patch('kustomize.commands.apply.apply')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'apply', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('kustomize.commands.apply.binarypath')
@patch('kustomize.commands.apply.shell')
def test_uses_shell(mock_shell, mock_binarypath):
    """
    Does command use the shell function to run commands?
    """
    kustomize.commands.apply.apply(['foo', 'bar'], None)

    assert mock_binarypath.mock_calls[0] == \
        call('kustomize', download_if_missing=True), \
        "We don't ensure all binaries are available"

    assert mock_shell.called, "Doesn't use shell() function"
