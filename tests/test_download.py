"""
Tests for the download helper module
"""
import platform
import responses

from unittest.mock import patch

import kustomize


def test_kubeval_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.download.GithubReleases('kubeval')

    assert dl.releases == \
        'https://github.com/instrumenta/kubeval/releases'
    assert dl.binary == (
        'kubeval.exe' if platform.system() == 'Windows' else 'kubeval')


def test_kustomize_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.download.GithubReleases('kustomize')

    assert dl.releases == \
        'https://github.com/kubernetes-sigs/kustomize/releases'
    assert dl.binary == (
        'kustomize.exe' if platform.system() == 'Windows' else 'kustomize')


@responses.activate
def test_lateststable_version():
    """
    Do we extract version string correctly from the GitHub API response?
    """
    responses.add(
        responses.HEAD,
        'https://github.com/kubernetes-sigs/kustomize/releases/latest',
        headers={
            'location':
                'https://github.com/kubernetes-sigs/kustomize/releases/v1.2.3'
        })

    dl = kustomize.download.GithubReleases('kustomize')
    version = dl.get_lateststable_version()

    assert version == 'v1.2.3', \
        "Version is not properly extracted from GitHub response"


@responses.activate
@patch('kustomize.download.GithubReleases.get_lateststable_version',
       return_value='v1.2.3')
@patch('kustomize.download.unpack_archive')
@patch('kustomize.download.NamedTemporaryFile')
def test_download(mock_tempfile, mock_unpackarchive, mock_version):
    """
    Do we try to download the archive and extract it locally?
    """
    dl = kustomize.download.GithubReleases('kustomize')
    dl.version = 'v1.2.3'
    dl_url = f"{dl.releases}/download/{dl.archive_schema}" % dl.__dict__
    dl_archive = dl_url.split('/')[-1]
    dl_targetdir = kustomize.binaries.binarypath()

    assert 'kustomize/v1.2.3/kustomize_v1.2.3_' in dl_url, \
        "Unexpected URL; mocked request will likely fail"

    responses.add(responses.GET, dl_url)
    dl.download()

    args, kwargs = mock_tempfile.call_args
    assert kwargs == dict(suffix=dl_archive, delete=False), \
        "Download of archive not attempted correctly"

    args, kwargs = mock_unpackarchive.call_args
    assert args[1] == dl_targetdir, \
        "Extraction to binaries folder not attempted correctly"
