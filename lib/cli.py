#!/usr/bin/env python3

import click
import helpers





@click.group()
def cli():
    """ Welcome to the Flatiron Dog Daycare CLI. 
    
    This app manages all the dogs checked into the daycare, as well as their information,
    owners, favorite toy, and other details 
    
    """

@cli.group()
def get():
    """Lists all subcommands for getting various data from the dogday care DB"""

@cli.group()
def update():
    """Lists all subcommands for updating various parameters within the DB"""


################################################
#   GETTER COMMANDS


## NEEED TO WORK ON THIS ##
@get.command()
@click.option('--name', type = click.STRING, help="search owner by NAME")
@click.option('--id', type = click.INT, required = True, default=0, help="search owner by ID")
def owner_info(name, id):
    "Search owner and provide details"
    click.echo('runs without parameters')

    if id:
        click.echo(id)
    else:
        click.echo(name)
    # get's the owner details, plus dog name + id
    # 

## NEEED TO WORK ON THIS ##
# @get.command()
# @click.option()
# def dog_info():
#     # get's the dog details, plus owner name + id
#     pass

## NEEED TO WORK ON THIS ##
# @get.command()
# @click.option()
# def toy_info():
#     # get's the toy's information
#     pass

## NEEED TO WORK ON THIS ##
# @get.command()
# @click.option()
# def breed_info():
#     # get's the breed's information
#     pass

@get.command()
def most_breeds():
    """Return breeds from most to least number in the daycare"""
    dogs = helpers.all_dogs()
    breed_dict = helpers.build_count_dict(dogs, "breed")

    breed_dict = sorted(breed_dict.items(), key=lambda x: x[1], reverse=True)
    helpers.print_all(breed_dict)


@get.command()
def most_favorite_toys():
    """Returns dog's favorite toys from most to least favorite"""
    dogs = helpers.all_dogs()
    toy_dict = helpers.build_count_dict(dogs, "toy")

    toy_dict = sorted(toy_dict.items(), key=lambda x : x[1], reverse=True)
    click.echo("Here are the most to least favorite toys in the daycare")
    click.echo("Toys, # of dogs that like it")
    helpers.print_all(toy_dict)


@get.command()
def most_dog_owners():
    """Returns the owners with the most to least amount of dogs"""

    owners = helpers.all_owners()
  
    owner_dict = {owner.name : len(owner.dogs) for owner in owners}
    owner_dict = sorted(owner_dict.items(), key=lambda x :x[1], reverse=True) 
    #dict.items() returns a tuple. Use index to access 2nd element to sort


    click.echo("Here is the list of owners with most to least amount of dogs:")
    click.echo("Owner, # of dogs")
    helpers.print_all(owner_dict)


@get.command()
def all_dogs():
    """Prints out all the dogs in the daycare center"""
    dogs = helpers.all_dogs()

    helpers.print_all(dogs)

@get.command(short_help="prints all owners")
def all_owners():
    """Prints out all the owners in the daycare center"""
    
    owners = helpers.all_owners()
    helpers.print_all(owners)


@get.command()
def all_toys():
    """Prints out all the toys in the daycare center"""
    
    toys = helpers.all_toys()
    helpers.print_all(toys)

if __name__ == "__main__":
    cli()