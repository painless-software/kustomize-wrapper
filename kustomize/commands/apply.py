"""
Apply manifest built by kustomize
"""
from ..helpers.binaries import binarypath, shell
from ..helpers.download import ensure_binary


def apply(folders, edit):
    """
    Apply manifests built by kustomize to the Kubernetes cluster
    """
    ensure_binary('kustomize')

    kustomize = binarypath('kustomize')
    kubectl_apply = "kubectl apply -f -"
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list} | {kubectl_apply}"

    if edit:
        pass

    shell(exec_string)
