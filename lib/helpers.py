from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

import click

engine = create_engine("sqlite:///db/dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


MODELS_DICT = {
        "dog" : Dog,
        "toy" : Toy,
        "breed" : Breed,
        "owner" : Owner
    }

def create_record(record, parameter):
    model = MODELS_DICT[parameter]

    confirm = click.confirm(f"Confirm to add a new {parameter} with the following details? \n{record}")
    
    if confirm:
        new_record = model(**record)
        session.add(new_record)
        session.commit()
        click.echo(f"The following has been added: {new_record}")
    else:
        click.echo("Action aborted")



def update_record(record):
    session.add(record)
    session.commit()
    return record


def delete_record(id, parameter):
    model = MODELS_DICT[parameter]
    
    record = session.query(model).filter(model.id == id).first()
    session.delete(record)
    session.commit()

def search_record(search, parameter):
    model = MODELS_DICT[parameter]
    record = session.query(model).filter(model.name.like(f"%{search}%")).all()
    return record


def return_record(id, parameter):
    
    model = MODELS_DICT[parameter]
    record = session.query(model).filter(model.id == id).first()

    if not record:
        raise click.BadParameter(message =f"The ID {id} did not produce any {parameter} records" )
    return record


def build_count_dict(data, arg):
    build_dict = {}
    for element in data:
        if getattr(element, arg) in build_dict:
            build_dict[getattr(element, arg)] += 1
        else:
            build_dict[getattr(element, arg)] = 1

    return build_dict    

def get_all(parameter):
    model = MODELS_DICT[parameter]
    records = session.query(model).all()
    return records


def print_all(data):
    counter = 1
    for entry in data:
        click.echo(entry)
        if counter % 25 == 0:
            click.prompt("Press enter to continue browsing", default= " ", show_default=False)
        counter += 1
    click.echo("You have reached the end of the list")

def print_details(record_obj):

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
