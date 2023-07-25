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
def get_most_breeds():
    """Return from most to least the number of dog breeds in the daycare"""
    dogs = helpers.all_dogs()
    breed_dict = helpers.build_count_dict(dogs, "breed")

    breed_dict = sorted(breed_dict.items(), key=lambda x: x[1], reverse=True)
    helpers.print_all(breed_dict)


@cli.command
def get_most_favorite_toys():
    """Returns dog's favorite toys from most to least favorite"""
    dogs = helpers.all_dogs()
    toy_dict = helpers.build_count_dict(dogs, "toy")

    toy_dict = sorted(toy_dict.items(), key=lambda x : x[1], reverse=True)
    helpers.print_all(toy_dict)


@cli.command()
def get_owners_with_most_dogs():
    """Returns the owners with the most to least amount of dogs"""

    owners = helpers.all_owners()
  
    owner_dict = {owner.name : len(owner.dogs) for owner in owners}
    owner_dict = sorted(owner_dict.items(), key=lambda x :x[1], reverse=True) 
    #dict.items() returns a tuple. Use index to access 2nd element to sort


    click.echo("Here is the list of owners with most to least amount of dogs:")
    click.echo("Owner, # of dogs")
    helpers.print_all(owner_dict)


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