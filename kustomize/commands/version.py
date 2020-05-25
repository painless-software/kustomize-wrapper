"""
Supply version information of all components
"""
import sys

from .. import __version__
from ..helpers.binaries import binarypath, run_piped_commands
from ..helpers.download import binary_exists, ensure_binary


def version(update=False):
    """Show version of all shipped components"""
    print(f"kustomize-wrapper {__version__}")

    if update:
        download_binaries()

    if not binary_exists('kustomize'):
        print(f"Go binary {binarypath('kustomize')} not available.")
    if not binary_exists('kubeval'):
        print(f"Go binary {binarypath('kubeval')} not available.")

    kustomize_result = run_piped_commands(
        [f"{binarypath('kustomize')} version"])
    kubeval_result = run_piped_commands(
        [f"{binarypath('kubeval')} --version"])

    if kustomize_result.stdout:
        print(f"Kustomize {kustomize_result.stdout.strip()}")
    if kubeval_result.stdout:
        print(f"Kubeval {kubeval_result.stdout.strip()}")


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
