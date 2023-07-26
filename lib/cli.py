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

@cli.group()
def delete():
    """Lists all subcommands for deleting entities within the DB"""

@cli.group()
def create():
    """Lists all subcommands for creating entities"""


################################################
#   CREATE COMMANDS


################################################
#   UPDATE COMMANDS

@update.command()
@click.option("--dog-ID", required=True, type=click.INT)
@click.option("--new-owner-ID", required=True, type=click.INT)
def dog_owner(dog_id, new_owner_id):
    """Updates the owner of the dog."""

    # prompt for new owner 
    # --ownerID
    # --dogID 

    # check for each ID if it's valid

    new_owner = helpers.return_owner(new_owner_id)
    dog = helpers.return_dog(dog_id)

    if not new_owner:
        click.echo(f"Owner ID input '{new_owner_id}' does not exist")
        return
    elif not dog:
        click.echo(f"Dog ID input '{dog_id}' does not exist")
        return
    
    message = f"Update DOG '{dog.name}' from it's OWNER {dog.owner.name}, ID {dog.owner.id} to NEW OWNER {new_owner.name}, ID {new_owner.id}"

    confirm_update = click.confirm(message)

    if confirm_update:
        updated_dog = helpers.update_dog_owner(dog, new_owner)
        click.echo("Update successful")
        click.echo(f"{updated_dog} now has owner {updated_dog.owner}")
    else:
        click.echo("Update aborted")



################################################
#   DELETE COMMANDS

@delete.command()
@click.option("--id", required=True, help="Deletes owners using ID")
def owner_record(id):
    """Delete's the owner record and dogs that they own from the system"""

    owner = helpers.return_owner(id)
    if owner:
        click.echo(owner)
        for dog in owner.dogs:
            click.echo(dog)
        confirm_delete = click.confirm("Are you sure you want to delete this record and subrecords?")
    else:
        click.echo("ID produced no owner record")
        return
    
    if confirm_delete:
        helpers.delete_owner(id)
        click.echo("Record successfully deleted")
    else:
        click.echo("Action aborted")

@delete.command()
@click.option('--id', required=True, help="Delete's dog record using ID")
def dog_record(id):
    """Delete's the dog record from the owner. Owner record stays in the system"""

    # pull record of dog
    # confirm if you want to delete this dog
    dog = helpers.return_dog(id)
    if dog:
        click.echo(dog)
        confirm_delete = click.confirm("Are you sure you want to delete this record?")
        
    else:
        click.echo("ID produced no dog record")
        return
    
    if confirm_delete:
        helpers.delete_dog(id)
        click.echo("Record successfully deleted")
    else:
        click.echo("Action aborted")

################################################
#   GETTER COMMANDS

@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name")
def search_for_toy(name):
    """Searches toys by names"""
    result = helpers.search_toy(name)
    helpers.print_all(result)

@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name")
def search_for_dog(name):
    """Searches dogs by names"""
    result = helpers.search_dog(name)
    helpers.print_all(result)

@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name")
def search_for_owner(name):
    """Searches owners by names"""
    result = helpers.search_owner(name)
    helpers.print_all(result)

@get.command()
@click.option("--id", type= click.INT, required=True, help="Use owner ID")
def info_owner(id):
    "Return owner info"
    owner = helpers.return_owner(id)

    if not owner:
        click.echo("ID produced no results")
    else:
        click.echo(f"Name: {owner.name}")
        click.echo(f"Phone: {owner.phone}")
        click.echo(f"Email: {owner.email}")
        click.echo(f"Address: {owner.address}")
        click.echo(f"{owner.name} owns the following dogs: ")
        for dog in owner.dogs:
            click.echo(dog)

@get.command()
@click.option("--id", type=click.INT, required=True, help="Use dog ID")
def info_dog(id):
    "Return dog info"
    dog = helpers.return_dog(id)

    if not dog:
        click.echo("ID produced no results")
    else:
        click.echo(f"Dog Name: {dog.name}")
        click.echo(f"Age: {dog.age}")
        click.echo(f"Checked in: {True if dog.checked_in else False}")
        click.echo(f"Owner: {dog.owner.name}, ID: {dog.owner.id}")
        click.echo(f"Favorite Toy: {dog.toy.color} {dog.toy.name}")
        click.echo(f"Breed: {dog.breed.name}")


@get.command()
@click.option("--id", type=click.INT, required=True, help="Use toy ID")
def info_toy(id):
    "Return toy info"
    toy = helpers.return_toy(id)

    if not toy:
        click.echo("ID produced no results")
    else:
        click.echo(f"Toy: {toy.color} {toy.name}")
        click.echo(f"Broken: {toy.broken}")


@get.command()
@click.option("--id", type=click.INT, required=True, help="Use toy ID")
def info_breed(id):
    "Return breed info"
    breed = helpers.return_breed(id)

    if not breed:
        click.echo("ID produced no results")
    else:
        click.echo(f"Breed: {breed.name}")
        click.echo(f"Hair Length: {breed.hair_length}")


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