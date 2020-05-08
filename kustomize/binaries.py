"""
Helper functions managing the included external binaries
"""
import os
import platform
import sys

from pathlib import Path
from subprocess import CalledProcessError, PIPE, run


def realpath(command):
    """
    Return the full path of an executable shipped with this package.
    Also appends the ".exe" extension if we're running on Windows.
    """
    binary_folder = \
        Path(sys.prefix) / 'shared' / 'bin' / platform.system().lower()
    command += '.exe' if platform.system() == 'Windows' else ''
    return binary_folder / command


def shell(command, silent=False):
    """
    Run a shell command with pipes and print it out, beautified, beforehand.
    """
    location = str(realpath('_').parent) + os.path.sep

    if not silent:
        beautified_command = command.replace(location, '')
        print(beautified_command)

    commands = [cmd.strip() for cmd in command.split('|')]
    last_output = None

    for cmd in commands:
        try:
            result = run(cmd.split(),
                         check=True,
                         input=last_output,
                         stderr=PIPE,
                         stdout=PIPE,
                         universal_newlines=True)
            last_output = result.stdout
        except CalledProcessError as err:
            raise SystemExit(err.output)
        except FileNotFoundError as err:
            raise SystemExit(err)

    if not silent:
        print(last_output)

    return last_output
