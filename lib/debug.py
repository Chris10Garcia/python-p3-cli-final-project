#!/usr/bin/env python3


from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from faker import Faker

from db.models import Owner, Dog, Breed, Toy

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/dog_daycare.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb; ipdb.set_trace()