"""
Tests for the download helper module
"""
import pathlib
import platform
import pytest
import responses

from unittest.mock import call, patch

import kustomize


def test_binary_versions_in_readme():
    """
    Have the binary version badges been updated in the README?
    """
    project_readme = pathlib.Path(__file__).parent.parent / 'README.md'
    kubeval_version = \
        kustomize.helpers.download.GithubReleases('kubeval').version
    kustomize_version = \
        kustomize.helpers.download.GithubReleases('kustomize').version

    with project_readme.open() as document:
        readme = document.read()

    assert readme.count(kubeval_version) == 2, \
        f"README badge doesn't match Kubeval version {kubeval_version}"
    assert readme.count(kustomize_version) == 2, \
        f"README badge doesn't match Kustomize version {kustomize_version}"


def test_kubeval_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.helpers.download.GithubReleases('kubeval')

    assert dl.releases == \
        'https://github.com/instrumenta/kubeval/releases'
    assert dl.binary == (
        'kubeval.exe' if platform.system() == 'Windows' else 'kubeval')
    assert dl.version == \
        kustomize.helpers.download.BINARY_INFO['kubeval']['version']

    assert dl.download_url.startswith(dl.releases)
    assert dl.version in dl.download_url
    assert dl.name in dl.download_url


def test_kustomize_object():
    """
    Are correct values set in a downloader instance?
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')

    assert dl.releases == \
        'https://github.com/kubernetes-sigs/kustomize/releases'
    assert dl.binary == (
        'kustomize.exe' if platform.system() == 'Windows' else 'kustomize')
    assert dl.version == \
        kustomize.helpers.download.BINARY_INFO['kustomize']['version']

    assert dl.download_url.startswith(dl.releases)
    assert dl.version in dl.download_url
    assert dl.name in dl.download_url


@responses.activate
@patch('kustomize.helpers.download.unpack_archive')
@patch('kustomize.helpers.download.NamedTemporaryFile')
def test_download(mock_tempfile, mock_unpackarchive):
    """
    Do we try to download the archive and extract it locally?
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')
    dl_archive = dl.download_url.split('/')[-1]

    assert 'kustomize/v3.8.4/kustomize_v3.8.4_' in dl.download_url, \
        f"Unexpected URL; mocked request will likely fail:\n{dl.download_url}"

    responses.add(responses.GET, dl.download_url)
    dl.download()

    args, kwargs = mock_tempfile.call_args
    assert kwargs == dict(suffix=dl_archive, delete=False), \
        "Download of archive not attempted correctly"

    args, kwargs = mock_unpackarchive.call_args
    assert args[1] == kustomize.helpers.download.DOWNLOAD_PATH, \
        "Extraction to binaries folder not attempted correctly"


@responses.activate
@patch('builtins.SystemExit', side_effect=KeyboardInterrupt)
@patch('kustomize.helpers.download.unpack_archive',
       side_effect=PermissionError)
@patch('kustomize.helpers.download.NamedTemporaryFile')
def test_fail_gracefully(
        mock_tempfile, mock_unpackarchive, mock_systemexit):
    """
    If download or extraction fails we need to fail nicely.
    """
    dl = kustomize.helpers.download.GithubReleases('kustomize')
    responses.add(responses.GET, dl.download_url)

    assert 'kustomize/v3.8.4/kustomize_v3.8.4_' in dl.download_url, \
        f"Unexpected URL; mocked request will likely fail:\n{dl.download_url}"

    with pytest.raises(KeyboardInterrupt):
        dl.download()

    args, kwargs = mock_systemexit.call_args
    assert args[0].startswith("Extracting binary failed:")


@patch('builtins.print')
@patch('kustomize.helpers.download.GithubReleases')
@patch('pathlib.Path.unlink')
def test_update_binary_delete(mock_unlink, mock_downloader, mock_print):
    """
    Is deletion of local binary attempted before download?
    """
    kustomize.helpers.download.update_binary('foo')

    mock_unlink.called, "Deletion is not attempted"
    mock_print.mock_calls == [call('Go binary foo removed.')]
    mock_downloader.called, "Download is not attempted"


@patch('builtins.print')
@patch('kustomize.helpers.download.GithubReleases')
@patch('pathlib.Path.unlink', side_effect=OSError)
def test_report_deletefailed(mock_unlink, mock_downloader, mock_print):
    """
    Do we handle errors gracefully?
    """
    kustomize.helpers.download.update_binary('foo')

    args, _ = mock_print.call_args_list[0]
    binarypath = kustomize.helpers.download.DOWNLOAD_PATH / 'foo'
    assert args[0].split(' failed. ')[0] == f"Deleting {binarypath}"
