from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

import click

engine = create_engine("sqlite:///db/dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


# Provides an easy way to select the Class and abstract helper functions
MODELS_DICT = {
        "dog" : Dog,
        "toy" : Toy,
        "breed" : Breed,
        "owner" : Owner
    }

def validate_inputs(attribute, value):
    """
    Validates an attribue's value.
    Checks for int's, if a record exisits, and boolean fasly / truthy
    """

    #checks for int
    if attribute == "breed_id" or attribute == "toy_id" or attribute == "owner_id" or attribute == "age" or attribute == "days_checked_in":
        try:
            int(value, 10)
        except:
            raise click.BadParameter(message = f"The {attribute} property require's an integer value")
    
    #checks if toy, owner or breed exits
    if attribute == "breed_id" or attribute == "toy_id" or attribute == "owner_id":
        return_record(value, attribute.replace("_id", ""))


    #check and fixes for truth or false
    #can fix and return boolean
    truthy = ('y', "true", "yes", "t", "1")
    falsy = ('n', "false", "no", "f", "0")
    if attribute == "checked_in" or attribute == "broken":
        if value.lower() in truthy:
            value = True
            return value
        elif value.lower() in falsy:
            value = False
            return value
        else:
            raise click.BadParameter(f"checked_in attribute requires true/false, t/f, yes/no, y/n, or 1/0 answers (case insensitive)")


def confirm_change(record, attribute, value):
    """
    Updates the db object with the provided attribute and value.
    Handles toy, breed, and owner changes.
    """

    # formats message to handle toy, breed, and owner changes for a dog record
    extra_info_new = None
    extra_info_current = None
    if attribute == "breed_id" or attribute == "toy_id" or attribute == "owner_id":
        current_owner_breed_toy = return_record(getattr(record, attribute), attribute.replace("_id", ""))
        new_owner_breed_toy = return_record(value, attribute.replace("_id", ""))
        extra_info_new = f" ({new_owner_breed_toy})"
        extra_info_current = f" ({current_owner_breed_toy})"

    # Creates message 
    message = f"Changing {getattr(record, 'name')}'s {attribute} " \
                f"from {getattr(record, attribute)}{extra_info_current if extra_info_current else ''} " \
                f"to {value}{extra_info_new if extra_info_new else ''}"

    confirm_update = click.confirm(message)

    if confirm_update:
        setattr(record, attribute, value)
        updated_record = update_record(record)
        click.echo(f"{updated_record.name}'s {attribute} is now {getattr(updated_record, attribute)}")
    else:
        click.echo("Update aborted")


def return_attributes(parameter):
    """
    Returns a list of attributes based on the class selected.
    Does not return attributes that are Magic Methods or SQLALC instances
    Does not return id, this is set by the DB.
    Does not return owner, dogs, toy, or breed attributes. These are objects set by the SQLALC ORM.
    """

    model = MODELS_DICT[parameter]

    keys = [key for key in model.__dict__ 
            if not key[0] == "_" and not key == "id" and not key == "owner" and not key == "dogs" and not key == "toy" and not key == "breed"]

    return keys


def create_record(record, parameter):
    """
    Create's a new record in the DB.
    If new dog record, checks if toy, breed, and owner exists.
    """

    model = MODELS_DICT[parameter]

    extra_info = None
    if parameter == "dog":
        toy = return_record(record["toy_id"], "toy")
        breed = return_record(record["breed_id"], "breed")
        owner = return_record(record["owner_id"], "owner")
        extra_info = f"\n{toy} \n{breed} \n{owner}\n"
    
    confirm = click.confirm(f"Confirm to add a new {parameter} with the following details? \n{record}{extra_info if extra_info else ''}")
    
    if confirm:
        new_record = model(**record)
        session.add(new_record)
        session.commit()
        click.echo(f"The following has been added: {new_record}")
    else:
        click.echo("Action aborted")


def update_record(record):
    """
    With a given updated db object, add's it to the db, commits, and returns the object
    """
    session.add(record)
    session.commit()
    return record


def delete_record(id, parameter):
    """
    Delete's a db record
    """

    model = MODELS_DICT[parameter]
    
    record = session.query(model).filter(model.id == id).first()
    session.delete(record)
    session.commit()

def search_record(search, parameter):
    """
    Searches for a db record based on name
    """

    model = MODELS_DICT[parameter]
    record = session.query(model).filter(model.name.like(f"%{search}%")).all()
    return record


def return_record(id, parameter):
    """
    Returns an existing record. If it does not exist, throw an error and exit program
    """
    model = MODELS_DICT[parameter]
    record = session.query(model).filter(model.id == id).first()

    if not record:
        raise click.BadParameter(message =f"The ID {id} did not produce any {parameter} records" )
    return record


def build_count_dict(data, arg):
    """
    Helper function to sum up how many breeds of a dog or how many toys of a dog.
    Returns dictionary of key (breed or toy) and total for each key 
    """

    build_dict = {}
    for element in data:
        if getattr(element, arg) in build_dict:
            build_dict[getattr(element, arg)] += 1
        else:
            build_dict[getattr(element, arg)] = 1

    return build_dict    


def get_all(parameter):
    """
    Return's all the db records for a given record type provided
    """

    model = MODELS_DICT[parameter]
    records = session.query(model).all()
    return records


def print_all(data):
    """
    Print's all of the object's within a given list.
    Prompt to continue every 25 records
    """

    counter = 1
    for entry in data:
        click.echo(entry)
        if counter % 25 == 0:
            click.prompt("Press enter to continue browsing", default= " ", show_default=False)
        counter += 1
    click.echo("You have reached the end of the list")


def print_details(record_obj):
    """
    Print's the attributes of a given record.
    Magic methods and SQLALC instance methods are not printed
    """
    record_dict = record_obj.__dict__

    for key, value in record_dict.items():
        if key == "_sa_instance_state" or key == "id":
            continue
        if key == "breed_id" or key=="owner_id" or key=="toy_id":
            click.echo(return_record(value, key.replace("_id", "")))
            continue
        click.echo(f"{key.capitalize()}: {value}")

    if isinstance(record_obj, Owner):
        click.echo("This person owns the following dogs")
        for dog in record_obj.dogs:
            click.echo(dog)
