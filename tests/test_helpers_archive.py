"""
Tests for the archive helper module
"""
from unittest.mock import call, patch

import pytest

import kustomize


@patch('kustomize.helpers.archive.unpack_zip_archive')
@patch('kustomize.helpers.archive.unpack_tar_archive')
def test_unpack_archive(mock_unpack_tar, mock_unpack_zip):
    """
    Are all supported archive types handled properly?
    """
    kustomize.helpers.archive.unpack_archive('/opt/foo.tar.gz', '/opt', 'bar')
    assert mock_unpack_tar.mock_calls == [
        call('/opt/foo.tar.gz', '/opt', 'bar')
    ]

    kustomize.helpers.archive.unpack_archive('/opt/foo.zip', '/opt', 'myfile')
    assert mock_unpack_zip.mock_calls == [
        call('/opt/foo.zip', '/opt', 'myfile')
    ]

    with pytest.raises(NotImplementedError):
        kustomize.helpers.archive.unpack_archive('/opt/foo.xyz', '/opt', 'baz')


@patch('tarfile.open')
def test_untar_files(mock_tarfile):
    """
    Are we looping through the file list correctly?
    """
    kustomize.helpers.archive.unpack_tar_archive(
        'foobar.tar.gz', '/opt', 'hello.sh', 'LICENSE')

    assert mock_tarfile.mock_calls == [
        call('foobar.tar.gz'),
        call().__enter__(),
        call().__enter__().extract('hello.sh', '/opt'),
        call().__enter__().extract('LICENSE', '/opt'),
        call().__exit__(None, None, None),
    ]


@patch('zipfile.ZipFile')
def test_unzip_files(mock_zipfile):
    """
    Are we looping through the file list correctly?
    """
    kustomize.helpers.archive.unpack_zip_archive(
        'foobar.zip', '/opt', 'afile.exe', 'README.md')

    assert mock_zipfile.mock_calls == [
        call('foobar.zip'),
        call().__enter__(),
        call().__enter__().extract('afile.exe', '/opt'),
        call().__enter__().extract('README.md', '/opt'),
        call().__exit__(None, None, None),
    ]
