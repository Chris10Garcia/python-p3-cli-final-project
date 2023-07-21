#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Owner, Dog, Breed, Toy

engine = create_engine("sqlite:///dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()

fake = Faker()

dog_temperaments = [
    "shy", "confident", "aggressive", "friendly", "responsive",
    "playful", "focused", "easily startled", "timid", "sad",
    "happy", "social", "anxious", "gentle", "silly", "calm", 
    "stubborn", "affectionate", "loyal", "lazy", "hyper",  
]

hair_length = [
    "short", "very short", "bald", "medium", "long", "extra-long"
]

def delete_records():
    session.query(Owner).delete()
    session.query(Dog).delete()
    session.query(Breed).delete()
    session.query(Toy).delete()
    session.commit()

def create_record():
    dogs = [Dog(
        name = fake.first_name(),
        age = random.randint(0,15),
        checked_in = fake.boolean(),
        temperament = fake.random_element(dog_temperaments)
    ) for x in range(30)]

    owners = [Owner(
        name = fake.name(),
        phone = fake.phone_number(),
        email = fake.email(),
        address = fake.street_address()
    ) for x in range(80)]
    

# create records

# relate_records

if __name__ == '__main__':
    delete_records()
    create_record()