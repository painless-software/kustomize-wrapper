"""
Tests for the command module
"""
import platform
import pytest

import kustomize.util


@pytest.mark.skipif(platform.system() != 'Linux', reason="requires Linux")
def test_realpath_linux():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.util.realpath('foo')
    assert '/bin/linux/' in str(path)


@pytest.mark.skipif(platform.system() != 'Darwin', reason="requires macOS")
def test_realpath_macos():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.util.realpath('foo')
    assert '/bin/darwin/' in str(path)


@pytest.mark.skipif(platform.system() != 'Windows', reason="requires Windows")
def test_realpath_windows():
    """
    Is path to shipped binaries calculated properly?
    """
    path = kustomize.util.realpath('foo')
    assert '\\bin\\windows\\' in str(path)


def test_binaries():
    """
    Are binaries available (cross-platform) from the calculated realpath?
    """
    kustomize_excutable = kustomize.util.realpath('kustomize')
    kubeval_executable = kustomize.util.realpath('kubeval')

    assert kustomize_excutable.is_file()
    assert kubeval_executable.is_file()
