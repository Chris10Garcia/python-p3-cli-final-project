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
def create():
    """Lists all subcommands for creating entities"""

@cli.group()
def get():
    """Lists all subcommands for getting various data from the dogday care DB"""

@cli.group()
def update():
    """Lists all subcommands for updating various parameters within the DB"""

@cli.group()
def delete():
    """Lists all subcommands for deleting entities within the DB"""




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
# READ COMMANDS                  #
##################################


@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name", prompt=True)
@click.option("--parameter", type=click.Choice(["dog", "breed", "toy", "owner"]), required=True, prompt=True)
def search_by_name(name, parameter):
    """NEED TO UPDATE THIS"""
    result = helpers.search_record(name, parameter)
    helpers.print_all(result)


@get.command()
@click.option("--id", type=click.INT, required=True, prompt=True)
@click.option("--parameter", type=click.Choice(["dog", "breed", "toy", "owner"]), required=True, prompt=True)
def print_details_for(id, parameter):
    """NEED TO UPDATE THIS"""
    record = helpers.return_record(id, parameter)
    helpers.print_details(record)

#parameter can be only breed, toy, dogs
@get.command()
@click.option("--parameter", type=click.Choice(("popular_breed", "favorite_toy", "most_dog")), required=True, prompt=True)
def most_by(parameter):
    """NEED TO UPDATE THIS"""
    if parameter == "popular_breed" or parameter == "favorite_toy":
        dogs = helpers.get_all("dog")
        param_formated = parameter[parameter.find("_")+1:]
        records_dict = helpers.build_count_dict(dogs, param_formated)
        message = "Here are the most popular breeds" if parameter == "popular_breed" else "Here are the most favorited toys"
    else:
        owners = helpers.get_all("owner")
        records_dict = {owner.name : len(owner.dogs) for owner in owners}
        message = "Here are the owners with the most dogs"

    sorted_records = sorted(records_dict.items(), key=lambda x: x[1], reverse=True)

    click.echo(message)
    helpers.print_all(sorted_records)



@get.command()
@click.option("--parameter", "-p", type=click.Choice(["dog", "owner", "breed", "toy"]), required=True, help="select the type of record to browse", prompt=True)
def all_records_by(parameter):
    """Prints out all records based on input parameter"""
    records = helpers.get_all(parameter)
    helpers.print_all(records)



##################################
# UPDATE COMMANDS                #
##################################

###########################
# TESTING CODE OUT. TRYING TO REFACTOR UPDATING ATTRIBUTES TO A MORE PROGRAMATTIC WAY
@update.command()
@click.option("--id", required=True, type=click.INT, prompt=True)
@click.option("--parameter", type=click.Choice(("dog", "owner")), prompt=True)
def test_update(id, parameter):
    """NEED TO UPDATE THIS"""
    record = helpers.return_record(id, parameter)

    keys = [key for key in record.__dict__ if not key == "_sa_instance_state" and not key == "id"]
    # results = [click.prompt(key) for key in keys]
    attribute = click.prompt("Pick attribute to update", type=click.Choice(keys))
    click.echo(attribute)
#######################################


## UPDATES DOG ATTRIBUTES
@update.command()
@click.option("--id", required=True, type=click.INT)
@click.option("--attribute", "-attr", required=True, type=click.Choice(["name", "age", "temperament", "checked_in", "breed_id", "toy_id"]), )
@click.option("--value", "-v", required=True, help="multi value inputs must be covered in quotes", metavar="'VALUE IN QUOTES'")
def attribute_dog(attribute, id, value):
    """Change the details of an exisiting dog"""
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

@delete.command()
@click.option("--id", type=click.INT, required=True, prompt=True)
@click.option("--parameter", type=click.Choice(("dog", "owner")), required=True, prompt=True)
def record_from_db(id, parameter):
    record = helpers.return_record(id, parameter)
    
    click.echo(record)
    if parameter == "owner":
        click.echo("Deleting an owner record will also delete the following dog records")
        for dog in record.dogs:
            click.echo(dog)

    confirm_delete = click.confirm("Are you sure you want to delete the above record(s)?")

    if confirm_delete:
        helpers.delete_record(id, parameter)
        click.echo("Record successfully deleted")
    else:
        click.echo("Action aborted")





if __name__ == "__main__":
    cli()