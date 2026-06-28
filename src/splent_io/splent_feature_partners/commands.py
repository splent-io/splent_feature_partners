"""
CLI commands contributed by splent_feature_partners.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:partners`` group.

Usage::

    splent feature:partners hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_partners!")


cli_commands = [hello]
