from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

import click

engine = create_engine("sqlite:///db/dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


def return_dog(id):
    dog = session.query(Dog).filter(Dog.id == id).first()
    return dog

def return_toy(id):
    toy = session.query(Toy).filter(Toy.id == id).first()
    return toy

def return_owner(id):
    owner = session.query(Owner).filter(Owner.id == id).first()
    return owner

def return_breed(id):
    breed = session.query(Breed).filter(Breed.id == id).first()
    return breed

# refactor so I can use this in other places
# do i need this????
def build_count_dict(data, arg):
    build_dict = {}
    for element in data:
        if getattr(element, arg) in build_dict:
            build_dict[getattr(element, arg)] += 1
        else:
            build_dict[getattr(element, arg)] = 1

    return build_dict    


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