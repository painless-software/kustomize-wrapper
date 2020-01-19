"""
Tests for the version module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import patch

import kustomize.version


@patch('kustomize.version.version')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'version'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called
