"""
Tests for the download helper module
"""
import platform
import pytest
import responses

from unittest.mock import call, patch

import kustomize


@patch('kustomize.helpers.download.GithubReleases')
def test_ensure_binary(mock_downloader):
    """
    Does function trigger download of a non-existing binary?
    """
    kustomize.helpers.download.ensure_binary('foo')

    assert mock_downloader.mock_calls == [
        call('foo'),
        call().download(),
    ]


def test_kubeval_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.helpers.download.GithubReleases('kubeval')

    assert dl.releases == \
        'https://github.com/instrumenta/kubeval/releases'
    assert dl.binary == (
        'kubeval.exe' if platform.system() == 'Windows' else 'kubeval')


def test_kustomize_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')

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

    dl = kustomize.helpers.download.GithubReleases('kustomize')
    version = dl.get_lateststable_version()

    assert version == 'v1.2.3', \
        "Version is not properly extracted from GitHub response"


@responses.activate
@patch('kustomize.helpers.download.GithubReleases.get_lateststable_version',
       return_value='v1.2.3')
@patch('kustomize.helpers.download.unpack_archive')
@patch('kustomize.helpers.download.NamedTemporaryFile')
def test_download(mock_tempfile, mock_unpackarchive, mock_version):
    """
    Do we try to download the archive and extract it locally?
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')
    dl.version = 'v1.2.3'
    dl_url = f"{dl.releases}/download/{dl.archive_schema}" % dl.__dict__
    dl_archive = dl_url.split('/')[-1]
    dl_targetdir = kustomize.helpers.binaries.binarypath()

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


@responses.activate
@patch('builtins.SystemExit', side_effect=KeyboardInterrupt)
@patch('kustomize.helpers.download.GithubReleases.get_lateststable_version',
       return_value='v1.2.3')
@patch('kustomize.helpers.download.unpack_archive',
       side_effect=PermissionError)
@patch('kustomize.helpers.download.NamedTemporaryFile')
def test_fail_gracefully(
        mock_tempfile, mock_unpackarchive, mock_version, mock_systemexit):
    """
    If download or extraction fails we need to fail nicely.
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')
    dl.version = 'v1.2.3'
    dl_url = f"{dl.releases}/download/{dl.archive_schema}" % dl.__dict__
    responses.add(responses.GET, dl_url)

    assert 'kustomize/v1.2.3/kustomize_v1.2.3_' in dl_url, \
        "Unexpected URL; mocked request will likely fail"

    with pytest.raises(KeyboardInterrupt):
        dl.download()

    args, kwargs = mock_systemexit.call_args
    assert args[0].startswith("Extracting binary failed:")
