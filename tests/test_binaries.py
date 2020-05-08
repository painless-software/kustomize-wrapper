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


@patch('builtins.print')
@patch('kustomize.binaries.run')
def test_shell_piped_command(mock_run, mock_print):
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
    assert len(mock_run.mock_calls) == 2, \
        f"run() not called for each command in '{shell_command}'"


def test_shell_failing_command():
    """
    Does an invalid command print its output and exit cleanly?
    """
    with pytest.raises(SystemExit):
        kustomize.binaries.shell('/non/existing/command')
