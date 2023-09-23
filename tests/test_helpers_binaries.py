"""
Tests for the binaries helper module
"""
import os
from unittest.mock import call, patch

import pytest

import kustomize


@patch('builtins.print')
@patch('shutil.which', return_value=None)
@patch('kustomize.helpers.binaries.GithubReleases')
def test_binarypath_download_missing(mock_downloader, mock_which, mock_print):
    """
    Does function trigger download of a non-existing binary?
    """
    with pytest.raises(FileNotFoundError):
        kustomize.helpers.binaries.binarypath('foo', download_if_missing=True)

    assert mock_print.mock_calls == [
        call('Binary for foo not found. Attempting download ...'),
    ]
    assert mock_downloader.mock_calls == [
        call('foo'),
        call().download(),
    ]


@patch('kustomize.helpers.binaries.run')
def test_run_piped_commands(mock_run):
    """
    Is list of commands properly executed as a pipe?
    """
    command_list = ['foo abc', 'bar -v', 'baz']
    expected_calls = len(command_list)

    kustomize.helpers.binaries.run_piped_commands(command_list)

    assert len(mock_run.mock_calls) == expected_calls, \
        f"run() not called for each command in '{' | '.join(command_list)}'"


@patch('builtins.print')
@patch('kustomize.helpers.binaries.run_piped_commands')
def test_shell_command(mock_run_piped_commands, mock_print):
    """
    Is command printed and then executed?
    """
    executable = kustomize.helpers.download.DOWNLOAD_PATH / 'foo'
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
