"""
Tests for the version command module
"""
from platform import python_version
from unittest.mock import call, patch

import pytest
from cli_test_helpers import ArgvContext

import kustomize


@patch('kustomize.commands.version.version')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'version'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('kustomize.commands.version.update_binary')
def test_cli_update_option(mock_updatebinary):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'version', '--update'), \
            pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_updatebinary.mock_calls == [
        call('kustomize'),
        call('kubeval'),
    ]


@patch('builtins.print')
@patch('kustomize.commands.version.binarypath', side_effect=FileNotFoundError)
def test_explain_when_missing(mock_binaryexists, mock_print):
    """
    Do we explain that binaries are not available?
    """
    version = python_version()

    kustomize.commands.version.version()

    assert mock_print.mock_calls == [
        call(f"kustomize-wrapper {kustomize.__version__} (Python {version})"),
        call("Go binary 'kustomize' not available. Use --update to download."),
        call("Go binary 'kubeval' not available. Use --update to download."),
    ]


@patch('kustomize.commands.version.update_binary')
def test_ensure_binaries(mock_updatebinary):
    """
    Do we call the function to update the binaries?
    """
    kustomize.commands.version.version(update=True)

    assert mock_updatebinary.mock_calls == [
        call('kustomize'),
        call('kubeval'),
    ]
