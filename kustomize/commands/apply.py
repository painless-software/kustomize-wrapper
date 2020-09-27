"""
Apply manifest built by kustomize
"""
from ..helpers.binaries import binarypath, shell


def apply(folders, edit):
    """
    Apply manifests built by kustomize to the Kubernetes cluster
    """
    kustomize = binarypath('kustomize', download_if_missing=True)
    kubectl_apply = "kubectl apply -f -"
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list} | {kubectl_apply}"

    if edit:
        pass

    shell(exec_string)
