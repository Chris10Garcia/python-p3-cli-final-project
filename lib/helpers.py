from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

import click

engine = create_engine("sqlite:///db/dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


def build_owner_dict(dogs):
    owner_dict = {}
    for dog in dogs:
        if dog.owner in owner_dict:
            owner_dict[dog.owner] += 1
        else:
            owner_dict[dog.owner] = 1

    return owner_dict    


def print_all(data):
    counter = 1
    for entry in data:
        click.echo(entry)
        if counter % 25 == 0:
            click.prompt("Press enter to continue browsing", default= " ", show_default=False)
        counter += 1
    click.echo("You have reached the end of the list")

# pull all dogs from db
def all_dogs():
    dogs = session.query(Dog).all()
    return dogs

# pull all owners from db
def all_owners():
    owners = session.query(Owner).all()
    return owners

# pull all toys from db
def all_toys():
    toys = session.query(Toy).all()
    return toys