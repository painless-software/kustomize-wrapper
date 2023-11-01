"""
Supply version information of all components
"""
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from platform import python_version

from ..helpers.binaries import binarypath, run_piped_commands
from ..helpers.download import update_binary


def version(update=False):
    """Show version of all shipped components"""
    package_version = metadata.version("kustomize_wrapper")
    print(f"kustomize-wrapper {package_version} (Python {python_version()})")

    if update:
        update_binary('kustomize')
        update_binary('kubeval')

    try:
        kustomize_binary = binarypath('kustomize')
        kustomize_result = run_piped_commands(
            [f"{kustomize_binary} version"])

        ver = kustomize_result.stdout.split()[0].split('v')[1]
        print(f"Kustomize {ver} ({kustomize_binary})")
    except FileNotFoundError:
        print("Go binary 'kustomize' not available."
              " Use --update to download.")

    try:
        kubeval_binary = binarypath('kubeval')
        kubeval_result = run_piped_commands(
            [f"{kubeval_binary} --version"])

        ver = kubeval_result.stdout.split()[1]
        print(f"Kubeval {ver} ({kubeval_binary})")
    except FileNotFoundError:
        print("Go binary 'kubeval' not available."
              " Use --update to download.")
