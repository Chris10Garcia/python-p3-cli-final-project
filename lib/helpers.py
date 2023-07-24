from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Owner, Dog, Breed, Toy

engine = create_engine("sqlite:///dog_daycare.db")
Session = sessionmaker(bind = engine)
session = Session()


# pull all dogs from db
def all_dogs():
    pass

# pull all owners from db
def all_owners():
    pass

# pull all toys from db
def all_toys():
    pass