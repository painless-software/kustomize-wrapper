"""
Perform validation of manifest built by kustomize
"""
from ..binaries import realpath, shell


def lint(folders, edit, ignore_missing_schemas):
    """
    Verify whether manifests built by kustomize are valid
    """
    kustomize = realpath('kustomize')
    kubeval = realpath('kubeval')
    kubeval_options = ' '.join([
        '--strict',
        '--ignore-missing-schemas' if ignore_missing_schemas else '',
    ])

    if edit:
        pass

    status = 0
    for folder in folders:
        command = f"{kustomize} build {folder} | {kubeval} {kubeval_options}"
        status += shell(command).returncode

    raise SystemExit(status)
