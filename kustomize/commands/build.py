"""
Build manifest with kustomize
"""
from ..helpers.binaries import binarypath, shell


def build(folders, edit):
    """
    Build manifests with kustomize
    """
    kustomize = binarypath('kustomize', download_if_missing=True)
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list}"

    if edit:
        pass

    shell(exec_string)
