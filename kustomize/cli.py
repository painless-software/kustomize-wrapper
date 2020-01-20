"""
Kustomize wrapper CLI
"""
import click

from .commands import apply as apply_command
from .commands import lint as lint_command
from .commands import version as version_command


@click.group()
@click.version_option()
def main():
    """Kustomize wrapper"""


@main.command()
def version():
    """Show version information of all shipped components"""
    version_command.version()


@main.command()
@click.argument('folders', nargs=-1, required=True)
@click.option('--edit')
def apply(folders, edit):
    """Apply manifests built by kustomize to the Kubernetes cluster"""
    apply_command.apply(folders, edit)


@main.command()
@click.argument('folders', nargs=-1, required=True)
@click.option('--edit')
def lint(folders, edit):
    """Verify whether manifests built by kustomize are valid"""
    lint_command.lint(folders, edit)
