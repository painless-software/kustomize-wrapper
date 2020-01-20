"""
Tests for the apply command module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import patch

import kustomize.cli


@patch('kustomize.commands.apply.apply')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'apply', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called
