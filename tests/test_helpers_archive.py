"""
Tests for the archive helper module
"""
import pytest

from unittest.mock import call, patch

import kustomize


@patch('kustomize.helpers.archive.unpack_zip_archive')
@patch('kustomize.helpers.archive.unpack_tar_archive')
def test_unpack_archive(mock_unpack_tar, mock_unpack_zip):
    """
    Are all supported archive types handled properly?
    """
    kustomize.helpers.archive.unpack_archive('/tmp/foo.tar.gz', '/tmp', 'bar')
    assert mock_unpack_tar.mock_calls == [
        call('/tmp/foo.tar.gz', '/tmp', 'bar')
    ]

    kustomize.helpers.archive.unpack_archive('/tmp/foo.zip', '/tmp', 'myfile')
    assert mock_unpack_zip.mock_calls == [
        call('/tmp/foo.zip', '/tmp', 'myfile')
    ]

    with pytest.raises(NotImplementedError):
        kustomize.helpers.archive.unpack_archive('/tmp/foo.xyz', '/tmp', 'baz')


@patch('tarfile.open')
def test_untar_files(mock_tarfile):
    """
    Are we looping through the file list correctly?
    """
    kustomize.helpers.archive.unpack_tar_archive(
        'foobar.tar.gz', '/tmp', 'hello.sh', 'LICENSE')

    assert mock_tarfile.mock_calls == [
        call('foobar.tar.gz'),
        call().__enter__(),
        call().__enter__().extract('hello.sh', '/tmp'),
        call().__enter__().extract('LICENSE', '/tmp'),
        call().__exit__(None, None, None),
    ]


@patch('zipfile.ZipFile')
def test_unzip_files(mock_zipfile):
    """
    Are we looping through the file list correctly?
    """
    kustomize.helpers.archive.unpack_zip_archive(
        'foobar.zip', '/tmp', 'afile.exe', 'README.md')

    assert mock_zipfile.mock_calls == [
        call('foobar.zip'),
        call().__enter__(),
        call().__enter__().extract('afile.exe', '/tmp'),
        call().__enter__().extract('README.md', '/tmp'),
        call().__exit__(None, None, None),
    ]
