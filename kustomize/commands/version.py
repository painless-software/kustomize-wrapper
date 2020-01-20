"""
Supply version information of all components
"""
import os

from .. import __version__
from ..util import realpath


def version():
    """Show version of all shipped components"""
    print(f"Kustomize wrapper {__version__}")
    print(f"kustomize:")
    os.system(f"{realpath('kustomize')} version")
    print(f"kubeval:")
    os.system(f"{realpath('kubeval')} --version")
