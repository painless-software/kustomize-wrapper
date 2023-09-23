"""
Enhanced version of ``unpack_archive`` in a helper module

shutil.unpack_archive() handles various archive formats (e.g. .zip, .tgz),
but it only extracts the entire content of those files. We only want a
single file from the archive, but don't want to go the extra route using
Python's ``tarfile`` and ``zipfile`` modules, separately, in user code.
"""
import pathlib
import tarfile
import zipfile


def unpack_archive(filename, extract_dir, *files):
    """Unpack files from a Tar or Zip archive"""

    archive_method = {
        '.tar.gz': unpack_tar_archive,
        '.tgz': unpack_tar_archive,
        '.zip': unpack_zip_archive,
    }
    filetype = get_file_extension(filename)
    try:
        archive_method[filetype](filename, extract_dir, *files)
    except KeyError as err:
        msg = f"Archive not supported: {filetype}"
        raise NotImplementedError(msg) from err


def unpack_tar_archive(filename, extract_dir, *files):
    """Unpack files from a Tar archive"""
    with tarfile.open(filename) as archive:
        for member in files:
            archive.extract(member, extract_dir)


def unpack_zip_archive(filename, extract_dir, *files):
    """Unpack files from a Zip archive"""
    with zipfile.ZipFile(filename) as archive:
        for member in files:
            archive.extract(member, extract_dir)


def get_file_extension(filename):
    """
    Reliably determine relevant file extension of archive

    >>> get_file_extension("/opt/foo_v3.8.2_linux_amd64.tgz")
    '.tgz'
    >>> get_file_extension("/opt/foo_v1.2.3_darwin.1.212.tar.gz")
    '.tar.gz'
    >>> get_file_extension("/opt/2020.12.31_windows.1.007.zip")
    '.zip'
    """
    min_len, max_len = 3, 4
    ext_list = pathlib.Path(filename).suffixes
    good_exts = [_ for _ in ext_list[-2:]
                 if min_len <= len(_) <= max_len and _[1:].isalpha()]
    return ''.join(good_exts)
