"""
Kustomize wrapper CLI
"""
import click

from . import version as version_command


@click.group()
@click.version_option()
def main():
    """Kustomize wrapper"""


@main.command()
def version():
    """Show version information of all shipped components"""
    version_command.version()
