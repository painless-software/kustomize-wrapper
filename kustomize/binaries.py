"""
Helper functions managing the included external binaries
"""
import os
import platform
import sys

from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, PIPE, run


def realpath(command):
    """
    Return the full path of an executable shipped with this package.
    Also appends the ".exe" extension if we're running on Windows.
    """
    binary_folder = \
        Path(sys.prefix) / 'shared' / 'bin' / platform.system().lower()
    command += '.exe' if platform.system() == 'Windows' else ''
    return binary_folder / command


def run_piped_commands(commands: list) -> CompletedProcess:
    """
    Silently run a list of commands piping one's output into the next one.
    Aborts gracefully on error, setting a non-zero ``returncode`` on the
    returned object.
    """
    result = CompletedProcess(0, None)

    for cmd in commands:
        args = cmd.split()
        try:
            result = run(args,
                         check=True,
                         input=result.stdout,
                         stderr=PIPE,
                         stdout=PIPE,
                         universal_newlines=True)
        except CalledProcessError as err:
            return CompletedProcess(args, 1,
                                    stderr=err.stderr,
                                    stdout=err.stdout)
        except FileNotFoundError as err:
            return CompletedProcess(args, 1, stderr=str(err))

    return result


def shell(shell_command, fail=False):
    """
    Run a shell command with pipes and print it out, beautified, beforehand
    """
    location = str(realpath('_').parent) + os.path.sep
    beautified_command = shell_command.replace(location, '')
    print(beautified_command)

    commands = [cmd.strip() for cmd in shell_command.split('|')]
    result = run_piped_commands(commands)

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode:
        msg = result.stderr.strip()
        if fail:
            raise SystemExit(msg)
        print(msg, file=sys.stderr)

    return result
