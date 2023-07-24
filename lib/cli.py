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

    helpers.print_all(dogs)

@cli.command()
def get_all_owners():
    """Prints out all the owners in the daycare center"""
    owners = helpers.all_owners()

    helpers.print_all(owners)


@cli.command()
def get_all_toys():
    """Prints out all the toys in the daycare center"""
    toys = helpers.all_toys()

    helpers.print_all(toys)

if __name__ == "__main__":
    cli()