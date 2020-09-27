"""
Helper functions managing the included external binaries
"""
import errno
import os
import shutil
import sys

from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, PIPE, run

from .download import DOWNLOAD_PATH, GithubReleases


def binarypath(command='', download_if_missing=False):
    """
    Return the full path of an external binary used by this package.
    Also appends the ".exe" extension if we're running on Windows.
    """
    usr_local_bin = str(Path('/') / 'usr' / 'local' / 'bin')
    search_path = os.pathsep.join(
        [str(DOWNLOAD_PATH)] +
        os.defpath.split(os.pathsep) +
        [usr_local_bin])

    found = shutil.which(command, path=search_path)

    if download_if_missing and not found:
        print(f"Binary for {command} not found. Attempting download ...")
        GithubReleases(command).download()
        found = shutil.which(command, path=search_path)

    if not found:
        err_message = f"Go binary not found in paths {search_path}"
        raise FileNotFoundError(errno.ENOENT, err_message, command)

    return Path(found)


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


def shell(shell_command):
    """
    Run a shell command with pipes and print it out, beautified, beforehand
    """
    location = str(DOWNLOAD_PATH) + os.path.sep
    beautified_command = shell_command.replace(location, '')
    print(beautified_command)

    commands = [cmd.strip() for cmd in shell_command.split('|')]
    result = run_piped_commands(commands)

    if result.stdout and result.stdout.strip():
        print(result.stdout.strip(), file=sys.stdout)

    if result.stderr and result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    return result
