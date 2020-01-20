"""
Apply manifest built by kustomize
"""
from ..binaries import realpath, shell


def apply(folders, edit):
    """
    Apply manifests built by kustomize to the Kubernetes cluster
    """
    kustomize = realpath('kustomize')
    kubectl_apply = "kubectl apply -f -"
    folder_list = ' '.join(folders)
    exec_string = f"{kustomize} build {folder_list} | {kubectl_apply}"

    if edit:
        pass

    shell(exec_string)
