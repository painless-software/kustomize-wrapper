"""
Supply version information of all components
"""
from .. import __version__
from ..binaries import realpath, run_piped_commands


def version():
    """Show version of all shipped components"""
    kustomize_version = \
        run_piped_commands([f"{realpath('kustomize')} version"]).stdout.strip()
    kubeval_version = \
        run_piped_commands([f"{realpath('kubeval')} --version"]).stdout.strip()

    print(f"kustomize-wrapper {__version__}")
    print(f"Kustomize {kustomize_version}")
    print(f"Kubeval {kubeval_version}")
