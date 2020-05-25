"""
Kustomize wrapper CLI
"""
import click

from .commands import apply as apply_command
from .commands import build as build_command
from .commands import lint as lint_command
from .commands import version as version_command


@click.group()
@click.version_option()
def main():
    """Kustomize wrapper"""


@main.command()
@click.option('--update', is_flag=True,
              help='Download Go binaries from GitHub')
def version(update):
    """Show version information of all shipped components"""
    version_command.version(update)


@main.command()
@click.argument('folders', nargs=-1, required=True)
@click.option('--edit')
def apply(folders, edit):
    """Apply manifests built by kustomize to the Kubernetes cluster"""
    apply_command.apply(folders, edit)


@main.command()
@click.argument('folders', nargs=-1, required=True)
@click.option('--edit')
def build(folders, edit):
    """Build all manifests with kustomize"""
    build_command.build(folders, edit)


@main.command()
@click.argument('folders', nargs=-1, required=True)
@click.option('--edit')
@click.option('--fail-fast', is_flag=True, show_default=True,
              help='Stop processing immediately when an error occurs')
@click.option('--force-color/--disable-color', default=True,
              help='Force ANSI colors on non-terminals, or turn it off '
                   'always  [default: --force-color]')
@click.option('--ignore-missing-schemas', flag_value='ignore_missing_schemas',
              default=False, show_default=True,
              help='Skip validation for resource definitions without a schema')
def lint(folders, edit, fail_fast, force_color, ignore_missing_schemas):
    """Verify whether manifests built by kustomize are valid"""
    lint_command.lint(
        folders, edit, fail_fast, force_color, ignore_missing_schemas)
