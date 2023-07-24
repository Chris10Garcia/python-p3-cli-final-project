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

    for dog in dogs:
        click.echo(dog)


if __name__ == "__main__":
    cli()