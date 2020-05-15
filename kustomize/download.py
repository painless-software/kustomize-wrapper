"""
Helper class to download external binaries
"""
import platform

from shutil import unpack_archive
from tempfile import NamedTemporaryFile

import requests

from .binaries import binarypath

BINARY_INFO = {
    'kubeval': {
        'repo': 'https://github.com/instrumenta/kubeval',
        'archive': {
            'linux': '%(version)s/%(name)s-%(platform)s-amd64.tar.gz',
            'darwin': '%(version)s/%(name)s-%(platform)s-amd64.tar.gz',
            'windows': '%(version)s/%(name)s-%(platform)s-amd64.zip',
        },
    },
    'kustomize': {
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
        print(f"Binary for {command} not found. Attempting to download ...")
        GithubReleases(command).download()


class GithubReleases:
    """Download binaries from GitHub repo release page"""

    def __init__(self, binary_name):
        """Constructor"""
        binary_info = BINARY_INFO[binary_name]
        repo_url = binary_info['repo']

        self.releases = f"{repo_url}/releases"
        self.platform = platform.system().lower()
        self.archive_schema = binary_info['archive'][self.platform]
        self.binary = binary_name + (
            '.exe' if self.platform == 'windows' else '')
        self.name = binary_name
        self.version = None

    def get_lateststable_version(self):
        """Find out latest version number via the 'latest' location"""
        response = requests.head(f"{self.releases}/latest")
        version = response.headers['location'].split('/')[-1]
        return version

    def download(self):
        """
        Download binary archive and extract binary to target location
        """
        print(f"Fetching version information for '{self.name}' ...")
        self.version = self.get_lateststable_version()
        download_url = \
            f"{self.releases}/download/{self.archive_schema}" % self.__dict__
        filename = download_url.split('/')[-1]
        target_directory = binarypath()

        print(f"Downloading {download_url} ...")
        response = requests.get(download_url)
        try:
            archive = NamedTemporaryFile(suffix=filename, delete=False)
            archive.write(response.content)
            archive.close()
        except OSError as err:
            raise SystemExit(f"Download failed: {err}")

        print(f"Extracting from {archive.name}: "
              f"{self.binary} -> {target_directory} ...")
        try:
            unpack_archive(archive.name, target_directory)
        except OSError as err:
            raise SystemExit(f"Extracting binary failed: {err}\n"
                             "Try installing in --user space.")
