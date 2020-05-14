"""
Tests for the version command module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import call, patch

import kustomize


@patch('kustomize.commands.version.version')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'version'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('kustomize.commands.version.ensure_binary')
def test_ensure_binaries(mock_ensurebinary):
    """
    Do we ensure binaries are available?
    """
    kustomize.commands.version.version()

    assert mock_ensurebinary.mock_calls == [
        call('kustomize'),
        call('kubeval'),
    ], "We don't ensure all binaries are available"
