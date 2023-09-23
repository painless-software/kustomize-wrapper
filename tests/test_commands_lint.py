"""
Tests for the lint command module
"""
from unittest.mock import call, patch

import pytest
from cli_test_helpers import ArgvContext

import kustomize


@patch('kustomize.commands.lint.lint')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'lint', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called


@patch('kustomize.commands.lint.binarypath')
@patch('builtins.print')
def test_fail_fast(mock_print, mock_binarypath):
    """
    Is the correct code called when invoked with option?
    """
    with ArgvContext('kustomize', 'lint', '--fail-fast', 'folder'), \
            pytest.raises(SystemExit):
        kustomize.cli.main()

    args, _ = mock_print.call_args
    assert args == ('Validation of your manifests FAILED.',)


@patch('kustomize.commands.lint.binarypath')
@patch('kustomize.commands.lint.shell')
def test_uses_shell(mock_shell, mock_binarypath):
    """
    Does command use the shell function to run commands?
    """
    expected_calls = 3

    with pytest.raises(SystemExit):
        kustomize.commands.lint.lint(['foo', 'bar', 'baz'],
                                     edit=None,
                                     fail_fast=False,
                                     force_color=False,
                                     ignore_missing_schemas=False)

    assert mock_binarypath.mock_calls[:2] == [
        call('kustomize', download_if_missing=True),
        call('kubeval', download_if_missing=True),
    ], "We don't ensure all binaries are available"

    assert mock_shell.call_count == expected_calls, \
        "Should call shell() function 3 times"
