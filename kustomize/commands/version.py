"""
Supply version information of all components
"""
import sys

from platform import python_version

from .. import __version__
from ..helpers.binaries import binarypath, run_piped_commands
from ..helpers.download import binary_exists, ensure_binary


def version(update=False):
    """Show version of all shipped components"""
    print(f"kustomize-wrapper {__version__} (Python {python_version()})")

    if update:
        download_binaries()

    kustomize_binary = binarypath('kustomize')
    kubeval_binary = binarypath('kubeval')

    if not binary_exists('kustomize'):
        print(f"Go binary {kustomize_binary} not available.")
    if not binary_exists('kubeval'):
        print(f"Go binary {kubeval_binary} not available.")

    kustomize_result = run_piped_commands(
        [f"{kustomize_binary} version"])
    kubeval_result = run_piped_commands(
        [f"{kubeval_binary} --version"])

    if kustomize_result.stdout:
        ver = kustomize_result.stdout.split()[0].split('/v')[1]
        print(f"Kustomize {ver} ({kustomize_binary})")
    if kubeval_result.stdout:
        ver = kubeval_result.stdout.split()[1]
        print(f"Kubeval {ver} ({kubeval_binary})")


def download_binaries():
    """Ensure Go binaries are installed"""
    kustomize_binary = binarypath('kustomize')
    kubeval_binary = binarypath('kubeval')

    try:
        kustomize_binary.unlink()
        print(f"Go binary {kustomize_binary} removed.")
    except FileNotFoundError:
        pass  # can be replaced by ``unlink(missing_ok=True)`` in Python 3.8+
    except OSError as err:
        print(f"Deleting {kustomize_binary} failed. {err}", file=sys.stderr)
    ensure_binary('kustomize')

    try:
        kubeval_binary.unlink()
        print(f"Go binary {kubeval_binary} removed.")
    except FileNotFoundError:
        pass  # can be replaced by ``unlink(missing_ok=True)`` in Python 3.8+
    except OSError as err:
        print(f"Deleting {kubeval_binary} failed. {err}", file=sys.stderr)
    ensure_binary('kubeval')
