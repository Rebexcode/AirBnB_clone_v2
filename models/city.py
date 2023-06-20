#!/usr/bin/python3
""" City Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """ The city class Representation"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    else:
        name = ""
        state.id = ""

    def __init__(self, *args, **kwargs):
        """Initializes city"""
        super().__init__(*args, **kwargs)
