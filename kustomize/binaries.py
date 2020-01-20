"""
Helper functions managing the included external binaries
"""
import os
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


def shell(command):
    """
    Run a shell command and print it out, beautified, beforehand.
    """
    location = str(realpath('_').parent) + os.path.sep
    beautified_command = command.replace(location, '')

    print(beautified_command)
    os.system(command)
