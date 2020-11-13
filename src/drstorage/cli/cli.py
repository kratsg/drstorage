import logging
import click

from ..version import __version__
from .. import models

logging.basicConfig()
log = logging.getLogger(__name__)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
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
    while True:
        line = bytestream.read(model.size)
        if line:
            click.echo(str(model.parse(line)).replace("\n", ""))
        else:
            break
