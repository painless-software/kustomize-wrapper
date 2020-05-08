"""
Supply version information of all components
"""
from .. import __version__
from ..binaries import realpath, shell


def version():
    """Show version of all shipped components"""
    kustomize_version = shell(f"{realpath('kustomize')} version", silent=True)
    kubeval_version = shell(f"{realpath('kubeval')} --version", silent=True)

    print(f"kustomize-wrapper {__version__}")
    print(f"Kustomize {kustomize_version.strip()}")
    print(f"Kubeval {kubeval_version.strip()}")
