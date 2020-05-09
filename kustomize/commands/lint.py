"""
Perform validation of manifest built by kustomize
"""
from ..binaries import realpath, shell


def lint(folders, edit, fail_fast, force_color, ignore_missing_schemas):
    """
    Verify whether manifests built by kustomize are valid
    """
    kustomize = realpath('kustomize')
    kubeval = realpath('kubeval')
    kubeval_options = ' '.join([
        '--force-color' if force_color else '',
        '--ignore-missing-schemas' if ignore_missing_schemas else '',
        '--strict',
    ])

    if edit:
        pass

    status = 0
    for folder in folders:
        command = f"{kustomize} build {folder} | {kubeval} {kubeval_options}"
        status += shell(command, fail=fail_fast).returncode

    raise SystemExit(status)
