"""
Perform validation of manifest built by kustomize
"""
from ..binaries import realpath, shell


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

    shell(exec_string)
