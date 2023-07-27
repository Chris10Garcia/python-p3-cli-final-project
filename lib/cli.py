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


##################################
# CREATE COMMANDS                #
##################################


## CREATES NEW DOG

## can refactor this????
@create.command()
@click.option("--name", "-n", required=True, prompt=True)
@click.option("--age", required=True, type = click.INT, prompt=True)
@click.option("--temperament", "-temper", required=True, prompt=True)
@click.option("--owner-id",required=True, type=click.INT, prompt=True)
@click.option("--breed-id", required=True, type=click.INT, prompt=True)
@click.option("--toy-id", required=True, type=click.INT, prompt=True)
def new_dog(name, age, temperament, owner_id, breed_id, toy_id):
    """Creates new dog, OWNER MUST EXIST IN DB"""

    owner = helpers.return_record(owner_id, "owner")
    toy = helpers.return_record(toy_id, "toy")
    breed = helpers.return_record(breed_id, "breed")
    click.echo(f"New dog {name} will be added to: {owner}.")
    click.echo(f"Their breed will be {breed}.")
    click.echo(f"Their favorite toy will be {toy}")

    new_record = {
        "name": name,
        "age": age,
        "checked_in": True,
        "temperament": temperament,
        "days_checked_in" : 0,
        "owner_id" : owner_id,
        "breed_id" : breed_id,
        "toy_id" : toy_id
    }
    
    helpers.create_record(new_record, "dog")



## CREATES NEW OWNER

## can refactor this????
@create.command()
@click.option("--name", "-n", required=True)
@click.option("--phone", "-p", required=True)
@click.option("--email", "-em", required=True)
@click.option("--address", "-a", required=True)
def new_owner(name, phone, email, address):
    """Creates new owner"""
    new_record = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    
    helpers.create_record(new_record, "owner")


##################################
# UPDATE COMMANDS                #
##################################

## UPDATES DOG ATTRIBUTES
@update.command()
@click.option("--id", required=True, type=click.INT)
@click.option("--attribute", "-attr", required=True, type=click.Choice(["name", "age", "temperament", "checked_in", "breed_id", "toy_id"]), )
@click.option("--value", "-v", required=True, help="multi value inputs must be covered in quotes", metavar="'VALUE IN QUOTES'")
def attribute_dog(attribute, id, value):
    """Change the details of an exisiting owner"""
    dog = helpers.return_record(id, "dog")

    ## can refactor this??
    # checks to see if the toy or breed exists in the DB
    param = None
    if attribute == "breed_id":
        param = "breed_id".replace("_id", "")

    elif attribute == "toy_id":
        param = "toy_id".replace("_id", "")

    if param:
        item = helpers.return_record(value, param)
        click.echo(item)

    # TUPLE USED HERE
    # converts checked_in answers to boolean responds
    truthy = ('y', "true", "yes", "t", "1")
    falsy = ('n', "false", "no", "f", "0")
    if attribute == "checked_in":
        if value.lower() in truthy:
            value = True
        elif value.lower() in falsy:
            value = False
        else:
            raise click.BadParameter(f"checked_in attribute requires true/false, t/f, yes/no, y/n, or 1/0 answers (case insensitive)")

    # checks age if it's an integer
    if attribute == "age":
        try:
            value = int(value, 10)
        except:
            raise click.BadParameter(f"age attributes requires an integer value")

    message = f"Changing {getattr(dog, 'name')}'s {attribute} from {getattr(dog, attribute)} to {value}"

    confirm_update = click.confirm(message)

    if confirm_update:
        setattr(dog, attribute, value)
        updated_dog = helpers.update_record(dog)
        click.echo(f"{updated_dog.name}'s {attribute} is now {getattr(updated_dog, attribute)}")
    else:
        click.echo("Update aborted")



## UPDATES OWNER ATTRIBUTES
@update.command()
@click.option("--id", required=True, type=click.INT)
@click.option("--attribute", "-attr", required=True, type=click.Choice(["name", "phone", "email", "address"]), )
@click.option("--value", "-v", required=True, help="multi value inputs must be covered in quotes", metavar="'VALUE IN QUOTES'", type=click.STRING)
def attribute_owner(attribute, id, value):
    """Change the details of an exisiting owner"""
    owner = helpers.return_record(id, "owner")

    message = f"Changing {getattr(owner, 'name')}'s {attribute} from {getattr(owner, attribute)} to {value}"

    confirm_update = click.confirm(message)

    if confirm_update:
        setattr(owner, attribute, value)
        updated_owner = helpers.update_record(owner)
        click.echo(f"{updated_owner.name}'s {attribute} is now {getattr(updated_owner, attribute)}")
    else:
        click.echo("Update aborted")



@update.command()
@click.option("--dog-id", required=True, type=click.INT)
@click.option("--new-owner-id", required=True, type=click.INT)
def dog_owner(dog_id, new_owner_id):
    """Updates the owner of the dog."""

    new_owner = helpers.return_record(new_owner_id, "owner")
    dog = helpers.return_record(dog_id, "dog")
    
    message = f"Update DOG '{dog.name}' from it's OWNER {dog.owner.name}, ID {dog.owner.id} to NEW OWNER {new_owner.name}, ID {new_owner.id}"

    confirm_update = click.confirm(message)

    if confirm_update:
        dog.owner_id = new_owner.id
        updated_dog = helpers.update_record(dog)
        click.echo("Update successful")
        click.echo(f"{updated_dog} now has owner {updated_dog.owner}")
    else:
        click.echo("Update aborted")



##################################
# DELETE COMMANDS                #
##################################

## can refactor this
@delete.command()
@click.option("--id", required=True, help="Deletes owners using ID")
def owner_record(id):
    """Delete's the owner record and dogs that they own from the system"""

    owner = helpers.return_record(id, "owner")
    click.echo(owner)
    for dog in owner.dogs:
        click.echo(dog)

    confirm_delete = click.confirm("Are you sure you want to delete this record and subrecords?")
    
    if confirm_delete:
        helpers.delete_record(id, "owner")
        click.echo("Record successfully deleted")
    else:
        click.echo("Action aborted")

## can refactor this
@delete.command()
@click.option('--id', required=True, help="Delete's dog record using ID")
def dog_record(id):
    """Delete's the dog record from the owner. Owner record stays in the system"""

    # pull record of dog
    # confirm if you want to delete this dog
    dog = helpers.return_record(id, "dog")
    click.echo(dog)
    confirm_delete = click.confirm("Are you sure you want to delete this record?")
    
    if confirm_delete:
        helpers.delete_record(id, "dog")
        click.echo("Record successfully deleted")
    else:
        click.echo("Action aborted")

##################################
# READ COMMANDS                  #
##################################


@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name", prompt=True)
@click.option("--parameter", type=click.Choice(["dog", "breed", "toy", "owner"]), required=True, prompt=True)
def search_by_name(name, parameter):
    result = helpers.search_record(name, parameter)
    helpers.print_all(result)

@get.command()
@click.option("--id", type=click.INT, required=True, prompt=True)
@click.option("--parameter", type=click.Choice(["dog", "breed", "toy", "owner"]), required=True, prompt=True)
def print_details_for(id, parameter):
    record = helpers.return_record(id, parameter)
    helpers.print_details(record)



## can refactor this
@get.command()
def most_breeds():
    """Return breeds from most to least number in the daycare"""
    dogs = helpers.get_all("dog")
    breed_dict = helpers.build_count_dict(dogs, "breed")

    breed_dict = sorted(breed_dict.items(), key=lambda x: x[1], reverse=True)
    helpers.print_all(breed_dict)

## can refactor this
@get.command()
def most_favorite_toys():
    """Returns dog's favorite toys from most to least favorite"""
    dogs = helpers.get_all("dog")
    toy_dict = helpers.build_count_dict(dogs, "toy")

    # TUPLE USED HERE
    toy_dict = sorted(toy_dict.items(), key=lambda x : x[1], reverse=True)
    click.echo("Here are the most to least favorite toys in the daycare")
    click.echo("Toys, # of dogs that like it")
    helpers.print_all(toy_dict)

## can refactor this
@get.command()
def most_dog_owners():
    """Returns the owners with the most to least amount of dogs"""

    owners = helpers.get_all("owner")
  
    owner_dict = {owner.name : len(owner.dogs) for owner in owners}

    # TUPLE USED HERE
    owner_dict = sorted(owner_dict.items(), key=lambda x :x[1], reverse=True) 
    #dict.items() returns a tuple. Use index to access 2nd element to sort


    click.echo("Here is the list of owners with most to least amount of dogs:")
    click.echo("Owner, # of dogs")
    helpers.print_all(owner_dict)


@get.command()
@click.option("--parameter", "-p", type=click.Choice(["dog", "owner", "breed", "toy"]), required=True, help="select the type of record to browse", prompt=True)
def all_records_by(parameter):
    """Prints out all records based on input parameter"""
    records = helpers.get_all(parameter)
    helpers.print_all(records)


if __name__ == "__main__":
    cli()