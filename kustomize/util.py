"""
Wrapper commands and options
"""
import platform

from pathlib import Path


def realpath(command):
    """
    Return the full path of an executable shipped with this package
    """
    module_root = Path(__file__).parent.parent
    return module_root / 'bin' / platform.system().lower() / command
