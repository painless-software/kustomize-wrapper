"""
Tests for the binaries helper module
"""
import os
import sys

from pathlib import Path
from unittest.mock import patch

import kustomize


@patch('platform.system', return_value='Linux')
def test_binarypath(mock_platform):
    """
    Is path to shipped binaries calculated properly?
    """
    old_prefix = sys.prefix
    sys.prefix = '/some/path'

    path = kustomize.helpers.binaries.binarypath('foo')
    assert path == Path('/') / 'some' / 'path' / 'local' / 'bin' / 'foo'

    sys.prefix = old_prefix


@patch('kustomize.helpers.binaries.run')
def test_run_piped_commands(mock_run):
    """
    Is list of commands properly executed as a pipe?
    """
    command_list = ['foo abc', 'bar -v', 'baz']
    kustomize.helpers.binaries.run_piped_commands(command_list)

    assert len(mock_run.mock_calls) == 3, \
        f"run() not called for each command in '{' | '.join(command_list)}'"


@patch('builtins.print')
@patch('kustomize.helpers.binaries.run_piped_commands')
def test_shell_command(mock_run_piped_commands, mock_print):
    """
    Is command printed and then executed?
    """
    executable = kustomize.helpers.binaries.binarypath('foo')
    exec_location = str(executable.parent) + os.path.sep
    shell_command = f"{executable} --bar | {executable} baz"
    kustomize.helpers.binaries.shell(shell_command)

    assert mock_print.called, \
        "print() is never called"
    assert exec_location not in str(mock_print.mock_calls[0]), \
        "Output doesn't seem to be beautified"
    assert mock_run_piped_commands.called, \
        "run_piped_commands() is not called"


def test_shell_failing_returncode():
    """
    Does an invalid command return a failing status code?
    """
    result = kustomize.helpers.binaries.shell('/non/existing/command')

    assert result.returncode, \
        "Non-zero status code expected, zero received"
