#!/usr/bin/env python3

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Categories(Base):
    __tablename__ = "categories"
    ##columns##
    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name, 
        }

class Items(Base):
    __tablename__ = "items"
    ##columns##
    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(2500), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return{
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
        }
            

    

###insert at the end of file###

engine = create_engine('sqlite:///itemCatelog.db')

Base.metadata.create_all(engine)
