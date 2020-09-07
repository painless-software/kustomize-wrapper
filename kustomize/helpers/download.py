"""
Helper class to download external binaries
"""
import platform

from tempfile import NamedTemporaryFile

import requests

from .archive import unpack_archive
from .binaries import binarypath

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
        'version': 'v3.8.2',
        'repo': 'https://github.com/kubernetes-sigs/kustomize',
        'archive': {
            'linux': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
            'darwin': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
            'windows': '%(name)s/%(version)s/%(name)s_%(version)s_%(platform)s_amd64.tar.gz',
        },
    },
}


def binary_exists(command):
    """Check existance of binary on file system"""
    return binarypath(command).is_file()


def ensure_binary(command):
    """
    Download the command binary if it's not available for execution
    """
    if not binary_exists(command):
        print(f"Binary for {command} not found. Attempting download ...")
        GithubReleases(command).download()


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

        print(f"Extracting from {archive.name}: {binarypath() / self.binary}")
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
        target_directory = binarypath()
        try:
            unpack_archive(archive.name, target_directory, self.binary)
        except Exception as err:
            raise SystemExit(f"Extracting binary failed: {err}\n"
                             "Try installing in --user space.") from err
