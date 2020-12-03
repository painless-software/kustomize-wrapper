"""
Helper class to download external binaries
"""
import platform

from pathlib import Path
from tempfile import NamedTemporaryFile

import sys
import requests

from .archive import unpack_archive

BINARY_INFO = {
    'kubeval': {
        'version': '0.15.0',
        'repo': 'https://github.com/instrumenta/kubeval',
        'archive': {
            'linux': '%(version)s/%(name)s-%(platform)s-amd64.tar.gz',
            'darwin': '%(version)s/%(name)s-%(platform)s-amd64.tar.gz',
            'windows': '%(version)s/%(name)s-%(platform)s-amd64.zip',
        },
    },
    'kustomize': {
        'version': 'v3.8.7',
        'repo': 'https://github.com/kubernetes-sigs/kustomize',
        'archive': {
            'linux': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
            'darwin': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
            'windows': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
        },
    },
}

DOWNLOAD_PATH = Path(sys.prefix) / 'local' / 'bin'


class GithubReleases:
    """Download binaries from GitHub repo release page"""

    def __init__(self, binary_name):
        """Constructor"""
        binary_info = BINARY_INFO[binary_name]
        repo_url = binary_info['repo']

        self.releases = f"{repo_url}/releases"
        self.platform = platform.system().lower()
        self.binary = binary_name + (
            '.exe' if self.platform == 'windows' else '')
        self.name = binary_name
        self.version = binary_info['version']
        archive_schema = binary_info['archive'][self.platform]
        self.download_url = \
            f"{self.releases}/download/{archive_schema}" % self.__dict__

    def download(self):
        """
        Download binary archive and extract binary to target location
        """
        print(f"Downloading {self.download_url} ...")
        archive = self.fetch_archive()

        print(f"Extracting from {archive.name}: {DOWNLOAD_PATH / self.binary}")
        self.extract_binary(archive)

    def fetch_archive(self):
        """Fetch the release archive from GitHub"""
        response = requests.get(self.download_url)
        filename = self.download_url.split('/')[-1]
        try:
            archive = NamedTemporaryFile(suffix=filename, delete=False)
            archive.write(response.content)
            archive.close()
        except OSError as err:
            raise SystemExit(f"Download failed: {err}") from err
        return archive

    def extract_binary(self, archive):
        """Unpack the binary we want from the downloaded archive"""
        try:
            unpack_archive(archive.name, DOWNLOAD_PATH, self.binary)
        except Exception as err:
            raise SystemExit(f"Extracting binary failed: {err}\n"
                             "Try installing in --user space.") from err


def update_binary(command):
    """
    Download matching Go binary, remove existing one first.
    (Run this for 'kustomize' and 'kubeval' separately.)
    """
    binarypath = DOWNLOAD_PATH / command

    try:
        binarypath.unlink()
        print(f"Go binary {binarypath} removed.")
    except FileNotFoundError:
        pass  # can be replaced by ``unlink(missing_ok=True)`` in Python 3.8+
    except OSError as err:
        print(f"Deleting {binarypath} failed. {err}", file=sys.stderr)

    GithubReleases(command).download()
