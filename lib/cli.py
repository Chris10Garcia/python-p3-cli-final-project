#!/usr/bin/env python3

import click
import helpers


@click.group()
def cli():
    """ Welcome to the Flatiron Dog Daycare CLI. 
    
    This app manages all the dogs checked into the daycare, as well as their information,
    owners, favorite toy, and other details 
    
    """


@cli.command()
def get_all_dogs():
    """Prints out all the dogs in the daycare center"""
    dogs = helpers.all_dogs()

    counter = 1
    for dog in dogs:
        click.echo(dog)
        if counter % 50 == 0:
            click.prompt("Press enter to continue", default= " ", show_default=False)
        counter += 1

@cli.command()
def get_all_owners():
    """Prints out all the owners in the daycare center"""
    owners = helpers.all_owners()

    counter = 1
    for owner in owners:
        click.echo(owner)
        if counter % 20 == 0:
            click.prompt("Press enter to continue", default= " ", show_default=False)
        counter += 1


@cli.command()
def get_all_toys():
    """Prints out all the toys in the daycare center"""
    toys = helpers.all_toys()

    counter = 1
    for toy in toys:
        click.echo(toy)
        if counter % 20 == 0:
            click.prompt("Press enter to continue", default= " ", show_default=False)
        counter += 1

if __name__ == "__main__":
    cli()