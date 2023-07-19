from sqlalchemy import MetaData, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


convention = {"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    phone = Column(Integer())
    email = Column(String(80))
    address = Column(String())

    pets = relationship('Pet', backref=backref('owner'))

    def __repr__(self):
        # <Owner: Christian Garcia is a customer at Flatiron Dog Daycare>
        return f"<Owner: {self.name} is a customer at FIDD>"


class Pet(Base):

    __tablename__ = "pets"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    age = Column(Integer())
    checked_in = Column(Boolean())
    days_checked_in = Column(Integer())
    temperament = Column(String())

    toy_id = Column(Integer(), ForeignKey('toys.id'))
    breed_id = Column(Integer(), ForeignKey('breeds.id'))
    owner_id = Column(Integer(), ForeignKey('owners.id'))

    def __repr__(self):
        return f"<Pet: {self.name} is a {self.age} year old {self.temperament} dog at FIDD>"



class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    hair_length = Column(String())

    pets = relationship('Pet', backref=backref('breed'))

    def __repr__(self):
        # <Breed> The german shepard is a dog breed type found at FIDD
        pass


class Toy(Base):
    __tablename__ = "toys"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    color = Column(String())
    broken = Column(Boolean())

    pets = relationship('Pet', backref=backref('toy'))

    def __repr__(self):
        # <Toy> The red squeeky ball is a toy found at FIDD
        pass



