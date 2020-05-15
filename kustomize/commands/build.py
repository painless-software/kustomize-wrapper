"""
Build manifest with kustomize
"""
from ..helpers.binaries import binarypath, shell
from ..helpers.download import ensure_binary


def build(folders, edit):
    """
    Build manifests with kustomize
    """
    ensure_binary('kustomize')

    kustomize = binarypath('kustomize')
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list}"

    if edit:
        pass

    shell(exec_string)
