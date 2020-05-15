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


@patch('kustomize.commands.version.download_binaries')
def test_cli_update_option(mock_downloadbinaries):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'version', '--update'), \
            pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_downloadbinaries.called


@patch('builtins.print')
@patch('kustomize.commands.version.binary_exists', return_value=False)
def test_explain_when_missing(mock_binaryexists, mock_print):
    """
    Do we explain that binaries are not available?
    """
    kustomize_binary = kustomize.commands.version.binarypath('kustomize')
    kubeval_binary = kustomize.commands.version.binarypath('kubeval')

    kustomize.commands.version.version()

    assert mock_print.mock_calls == [
        call(f"kustomize-wrapper {kustomize.__version__}"),
        call(f"Go binary {kustomize_binary} not available."),
        call(f"Go binary {kubeval_binary} not available."),
    ]


@patch('pathlib.Path.unlink')
@patch('kustomize.commands.version.ensure_binary')
def test_ensure_binaries(mock_ensurebinary, mock_unlink):
    """
    Do we ensure binaries are available?
    """
    kustomize.commands.version.version(update=True)

    assert mock_ensurebinary.mock_calls == [
        call('kustomize'),
        call('kubeval'),
    ], "We don't ensure all binaries are available"


@patch('builtins.print')
@patch('kustomize.commands.version.ensure_binary')
@patch('pathlib.Path.unlink', side_effect=OSError)
def test_report_deletefailed(mock_unlink, mock_ensurebinary, mock_print):
    """
    Do we handle errors gracefully?
    """
    kustomize_binary = kustomize.commands.version.binarypath('kustomize')
    kubeval_binary = kustomize.commands.version.binarypath('kubeval')

    kustomize.commands.version.download_binaries()
    kust_args, _ = mock_print.call_args_list[0]
    kube_args, _ = mock_print.call_args_list[1]

    assert kust_args[0].split(' failed. ')[0] == f"Deleting {kustomize_binary}"
    assert kube_args[0].split(' failed. ')[0] == f"Deleting {kubeval_binary}"
