"""
Perform validation of manifest built by kustomize
"""
import os

from ..util import realpath


def lint(folders, edit):
    """
    Verify whether manifests built by kustomize are valid
    """
    kustomize = realpath('kustomize')
    kubeval = realpath('kubeval')
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list} | {kubeval} --strict"

    if edit:
        pass

    print(exec_string)
    os.system(exec_string)
