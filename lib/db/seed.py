
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Owner, Dog, Breed, Toy

engine = create_engine("sqlite:///dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()

fake = Faker()

# delete records

def delete_records():
    session.query(Owner).delete()
    session.query(Dog).delete()
    session.query(Breed).delete()
    session.query(Toy).delete()
    session.commit()

# create records

# relate_records