"""
Build manifest with kustomize
"""
from ..binaries import binarypath, shell


def build(folders, edit):
    """
    Build manifests with kustomize
    """
    kustomize = binarypath('kustomize')
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list}"

    if edit:
        pass

    shell(exec_string)
