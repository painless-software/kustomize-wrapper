"""
Supply version information of all components
"""
from .. import __version__
from ..binaries import binarypath, run_piped_commands
from ..download import ensure_binary


def version():
    """Show version of all shipped components"""
    print(f"kustomize-wrapper {__version__}")

    ensure_binary('kustomize')
    ensure_binary('kubeval')

    kustomize_result = run_piped_commands(
        [f"{binarypath('kustomize')} version"])
    kubeval_result = run_piped_commands(
        [f"{binarypath('kubeval')} --version"])

    if kustomize_result.stdout:
        print(f"Kustomize {kustomize_result.stdout.strip()}")
    if kubeval_result.stdout:
        print(f"Kubeval {kubeval_result.stdout.strip()}")
