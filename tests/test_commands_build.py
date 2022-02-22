"""
Tests for the build command module
"""
from unittest.mock import call, patch

import pytest
from cli_test_helpers import ArgvContext

import kustomize


@patch('kustomize.commands.build.build')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'build', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('kustomize.commands.build.binarypath')
@patch('kustomize.commands.build.shell')
def test_uses_shell(mock_shell, mock_binarypath):
    """
    Does command use the shell function to run commands?
    """
    kustomize.commands.build.build(['foo', 'bar'], None)

    assert mock_binarypath.mock_calls[0] == \
        call('kustomize', download_if_missing=True), \
        "We don't ensure all binaries are available"

    assert mock_shell.called, "Doesn't use shell() function"
