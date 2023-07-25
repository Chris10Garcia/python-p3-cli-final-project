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
    "short", "very short", "naked", "medium", "long", "extra-long"
]

toy_list = [
    "ball", "lamb plush", "pig plush", "moose plush", "big ball",
    "bacon flavor wishbone", "snake plush", "squirrel plush",
    "tug-n-toss", "teething chew toy", "treat dispensing toy",
    "challenge slider", "rope tug"
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
    ) for x in range(200)]

    # going to delete this once everything else is set up
    for dog in dogs:
        if dog.checked_in:
            dog.days_checked_in = random.randint(0, 29)


    owners = [Owner(
        name = fake.name(),
        phone = fake.phone_number(),
        email = fake.email(),
        address = fake.street_address()
    ) for x in range(60)]

    with open ("breeds.txt") as txt_file:
        breeds = [Breed(
                name = line.strip(),
                hair_length = fake.random_element(hair_length)
                ) for line in txt_file]
    
    toys = [Toy(
        name = fake.random_element(toy_list),
        color = fake.safe_color_name(),
        broken = fake.boolean(chance_of_getting_true=15)
    ) for x in range (20)]

    session.add_all(owners + breeds + toys + dogs)
    session.commit()

    return owners, breeds, toys, dogs

def relate_records(owners, breeds, toys, dogs):
    for dog in dogs:
        dog.toy_id = random.randint(1, len(toys))
        dog.breed_id = random.randint(1, len(breeds))
        dog.owner_id = random.randint(1, len(owners))

    session.add_all(dogs)
    session.commit()

if __name__ == '__main__':
    delete_records()
    owners, breeds, toys, dogs = create_record()
    relate_records(owners, breeds, toys, dogs)
