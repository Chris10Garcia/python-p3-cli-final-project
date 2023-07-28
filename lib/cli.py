#!/usr/bin/env python3

import click
import helpers


# Click Option Settings
# Many of these settings are repetated multiple times
# Keeping them in 1 spot to ensure consistency
PARAM_ALL = ("dog", "breed", "toy", "owner")
PARAM_DOG_OWNER = ("dog", "owner")
CLICK_ID_SETTINGS = (("--id", "-i"), 
                    {"required": True, "type" : click.INT, "prompt" : "Current ID", "help" : "Enter ID of record as an INT"})
CLICK_PARAM_SETTING_DOG_OWNER = (("--parameter", "-p"), 
                                 {"type" : click.Choice(PARAM_DOG_OWNER), "required": True, "prompt": "Select record type", 
                                  "help":"Select type of record to perform action on"})
CLICK_PARAM_SETTING_ALL = (("--parameter", "-p"), 
                           {"type" : click.Choice(PARAM_ALL), "required": True, "prompt": "Select record type", 
                            "help":"Select type of record to perform action on"})

@click.group()
def cli():
    """ Welcome to the Flatiron Dog Daycare CLI. 
    
    This app manages all the dogs within the daycare center. This includes:\n
    - Their owners: name, address, who owns which dogs\n
    - The dogs: their favorite toys, breed, age, checked in\n
    - And the toy plus breed lists and their information \n
    This app can perform CRUD actions on various records and record attributes.
    Please browse the help documentation for command options and require inputs.
    
    """

@cli.group()
def create():
    """Subcommands creates a new dog or owner record"""

@cli.group()
def get():
    """Subcommands gets (reads) dog, owner, toy, and breed info"""

@cli.group()
def update():
    """Subcommands updates attributes for a given record"""

@cli.group()
def delete():
    """Subcommands deletes a given dog or owner record"""



##################################################
#               CREATE COMMANDS                  #
##################################################


@create.command()
@click.option(*CLICK_PARAM_SETTING_DOG_OWNER[0], **CLICK_PARAM_SETTING_DOG_OWNER[1])
def new_dog_or_owner(parameter):
    """Add a new dog or owner to the DB. New dog records require an existing owner, toy, and breed record."""

    attributes = helpers.return_attributes(parameter)
    new_record_dict = {attr : click.prompt(f"Enter the value for the new {parameter}'s {attr}") for attr in attributes}

    for key, value in new_record_dict.items():
        helpers.validate_inputs(key, value)
        if key == "checked_in" or key == "broken":
            new_record_dict[key] = helpers.validate_inputs(key, value)

    helpers.create_record(new_record_dict, parameter)



##################################################
#             GETTER (READ) COMMANDS             #
##################################################


@get.command()
@click.option("--name", type=click.STRING, required=True, help="Search by name", prompt=True)
@click.option(*CLICK_PARAM_SETTING_ALL[0], **CLICK_PARAM_SETTING_ALL[1])
def search_by_name(name, parameter):
    """Search the database and returns records with names that contains the inputs provided. Case insensitive"""
    result = helpers.search_record(name, parameter)
    helpers.print_all(result)


@get.command()
@click.option(*CLICK_ID_SETTINGS[0], **CLICK_ID_SETTINGS[1])
@click.option(*CLICK_PARAM_SETTING_ALL[0], **CLICK_PARAM_SETTING_ALL[1])
def details_for(id, parameter):
    """Returns the record with a matching ID and print's all of it's details. Program aborts for nonexisting records"""
    record = helpers.return_record(id, parameter)
    helpers.print_details(record)


@get.command()
@click.option("--parameter", type=click.Choice(("popular_breed", "favorite_toy", "most_dog")), required=True, prompt=True)
def most_by(parameter):
    """Returns, from most to least, records that match the criteria provided: most popular breed, favorite toy, or owners with the most dogs"""
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
@click.option(*CLICK_PARAM_SETTING_ALL[0], **CLICK_PARAM_SETTING_ALL[1])
def all_records_for(parameter):
    """Returns and prints out all records based on input parameter"""
    records = helpers.get_all(parameter)
    helpers.print_all(records)

 

##################################################
#                UPDATE COMMANDS                 #
##################################################

@update.command()
@click.option(*CLICK_ID_SETTINGS[0], **CLICK_ID_SETTINGS[1])
@click.option(*CLICK_PARAM_SETTING_ALL[0], **CLICK_PARAM_SETTING_ALL[1])
def record_attribute(id, parameter):
    """Updates an existing record with the provided attribute and value.
    Toy, breed, and owner record must exist if changing these attributes for a dog's record 
    """
    record = helpers.return_record(id, parameter)

    keys = helpers.return_attributes(parameter)
    # results = [click.prompt(key) for key in keys]
    attribute = click.prompt("Pick attribute to update", type=click.Choice(keys))
    value = click.prompt(f"What will be the new value of this {attribute} property")

    helpers.validate_inputs(attribute, value)

    helpers.confirm_change(record, attribute, value)




##################################
# DELETE COMMANDS                #
##################################

@delete.command()
@click.option(*CLICK_ID_SETTINGS[0], **CLICK_ID_SETTINGS[1])
@click.option(*CLICK_PARAM_SETTING_DOG_OWNER[0], **CLICK_PARAM_SETTING_DOG_OWNER[1])
def record_from_db(id, parameter):
    """Delete's an exisiting dog or owner record from the DB. If deleting an owner, dog
    records belonging to the owner will also be deleted.
    IMPORTANT: DELETING A RECORD CAN NOT BE UNDONE.
    """

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