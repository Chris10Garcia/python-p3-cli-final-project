from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

import click

engine = create_engine("sqlite:///db/dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


def print_all(data):
    counter = 1
    for entry in data:
        click.echo(entry)
        if counter % 25 == 0:
            click.prompt("Press enter to continue browsing", default= " ", show_default=False)
        counter += 1

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