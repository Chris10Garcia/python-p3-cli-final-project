from sqlalchemy import MetaData, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


convention = {"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer(), primary_key=True)
    phone = Column(Integer())
    email = Column(String(80))
    address = Column(String())

    pets = relationship('Pet', backref=backref('owner'))

    def __repr__(self):
        pass
    
    """
    __tablename__ 

    table attributes

    pets = relationship

    def __repr__

    """

class Pet(Base):
    """
    __tablename__

    table attributes 
    + foriegn ID for owner id
    + foriegn ID for breed id
    + foriegn ID for toy id

    def __repr__
    """

    pass

class Breed(Base):
    """
    __tablename__

    table attributes 

    def __repr__
    """
    pass

class Toy(Base):
    """
    __tablename__

    table attributes 
    
    def __repr__
    """
    pass

