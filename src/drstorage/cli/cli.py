from __future__ import annotations

import logging

import click

from .. import models
from ..version import __version__

logging.basicConfig()
log = logging.getLogger(__name__)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def drstorage():
    pass


@drstorage.command()
@click.argument("bytestream", default="-", type=click.File("rb"))
@click.option(
    "--model",
    "-m",
    "model_name",
    help="The model to use for parsing",
    type=click.Choice(models.__all__),
    default=models.__all__[0],
)
def parse(bytestream, model_name):
    model = getattr(models, model_name)
    line = bytestream.read(model.size)
    while line:
        click.echo(str(model.parse(line)).replace("\n", ""))
        line = bytestream.read(model.size)
