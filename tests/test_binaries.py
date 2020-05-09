"""
Tests for the binaries helper module
"""
import os
import platform
import pytest

from unittest.mock import patch

import kustomize.binaries


@pytest.mark.skipif(platform.system() != 'Linux', reason="requires Linux")
def test_realpath_linux():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.binaries.realpath('foo')
    assert '/bin/linux/' in str(path)


@pytest.mark.skipif(platform.system() != 'Darwin', reason="requires macOS")
def test_realpath_macos():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.binaries.realpath('foo')
    assert '/bin/darwin/' in str(path)


@pytest.mark.skipif(platform.system() != 'Windows', reason="requires Windows")
def test_realpath_windows():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.binaries.realpath('foo')
    assert '\\bin\\windows\\' in str(path)


def test_binaries_available():
    """
    Are binaries available (cross-platform) from the calculated realpath?
    """
    kustomize_excutable = kustomize.binaries.realpath('kustomize')
    kubeval_executable = kustomize.binaries.realpath('kubeval')

    assert kustomize_excutable.is_file()
    assert kubeval_executable.is_file()


@patch('kustomize.binaries.run')
def test_run_piped_commands(mock_run):
    """
    Is list of commands properly executed as a pipe?
    """
    command_list = ['foo abc', 'bar -v', 'baz']
    kustomize.binaries.run_piped_commands(command_list)

    assert len(mock_run.mock_calls) == 3, \
        f"run() not called for each command in '{' | '.join(command_list)}'"


@patch('builtins.print')
@patch('kustomize.binaries.run_piped_commands')
def test_shell_command(mock_run_piped_commands, mock_print):
    """
    Is command printed and then executed?
    """
    executable = kustomize.binaries.realpath('foo')
    exec_location = str(executable.parent) + os.path.sep
    shell_command = f"{executable} --bar | {executable} baz"
    kustomize.binaries.shell(shell_command)

    assert mock_print.called, \
        "print() is never called"
    assert exec_location not in str(mock_print.mock_calls[0]), \
        "Output doesn't seem to be beautified"
    assert mock_run_piped_commands.called, \
        f"run_piped_commands() is not called"


def test_shell_failing_returncode():
    """
    Does an invalid command return a failing status code?
    """
    result = kustomize.binaries.shell('/non/existing/command')

    assert result.returncode, \
        "Non-zero status code expected, zero received"


def test_shell_failing_systemexit():
    """
    Does an invalid command abort execution when ``fail`` is set?
    """
    with pytest.raises(SystemExit):
        kustomize.binaries.shell('/non/existing/command', fail=True)
