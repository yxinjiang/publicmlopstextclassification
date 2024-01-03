import click

from textclassification.tasks.retrain_model import retrain_model
from textclassification.tasks.train_model import train_model

@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--partition-date",
    "-p",
    required=True,
    type=str,
    help="Specify the last partition date for training",
)
def train(partition_date):
    """Command to train the model."""
    click.echo(f"Training model with last partition date: {partition_date}")
    train_model(partition_date)

@click.command()
@click.option(
    "--partition-date",
    "-p",
    required=True,
    type=str,
    help="Specify the last partition date for training",
)
def retrain(partition_date):
    """Command to train the model."""
    click.echo(f"Retraining model with last partition date: {partition_date}")
    retrain_model(partition_date)


cli.add_command(train)
cli.add_command(retrain)

if __name__ == "__main__":
    cli(standalone_mode=False)
