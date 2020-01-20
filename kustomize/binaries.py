"""
Helper functions managing the included external binaries
"""
import platform
import sys

from pathlib import Path


def realpath(command):
    """
    Return the full path of an executable shipped with this package.
    Also appends the ".exe" extension if we're running on Windows.
    """
    binary_folder = \
        Path(sys.prefix) / 'shared' / 'bin' / platform.system().lower()
    command += '.exe' if platform.system() == 'Windows' else ''
    return binary_folder / command
