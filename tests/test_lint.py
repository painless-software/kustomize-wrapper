"""
Tests for the lint command module
"""
import pytest

from cli_test_helpers import ArgvContext
from unittest.mock import patch

import kustomize.cli


@patch('kustomize.commands.lint.lint')
def test_cli_command(mock_command):
    """
    Is the correct code called when invoked via the CLI?
    """
    with ArgvContext('kustomize', 'lint', '.'), pytest.raises(SystemExit):
        kustomize.cli.main()

    assert mock_command.called
