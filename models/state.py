#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class Representation """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="states")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes state"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") !== 'db':
        @property
        def cities(self):
            """FS attribute to return City instances"""
            values_city = models.storage.all("City").values()
            list_city = []
            for city in values_city:
                if city.state.id == self.id:
                    list_city.append(city)
            return list_city
