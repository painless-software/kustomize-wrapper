"""
Perform validation of manifest built by kustomize
"""
import sys

from ..helpers.binaries import binarypath, shell


def lint(folders, edit, fail_fast, force_color, ignore_missing_schemas):
    """
    Verify whether manifests built by kustomize are valid
    """
    kustomize = binarypath('kustomize', download_if_missing=True)
    kubeval = binarypath('kubeval', download_if_missing=True)
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
        status += shell(command).returncode
        if status and fail_fast:
            break

    if status:
        print("Validation of your manifests FAILED.", file=sys.stderr)
    raise SystemExit(status)
