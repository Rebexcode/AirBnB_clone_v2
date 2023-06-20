#!/usr/bin/pyhton3
"""
Database storage engine using SQLAlchemy with a mysql+mysqldb connection
"""

from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
nametoclass = {
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review,
        'User': User
        }


class DBStorage:
    """DB Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization of object"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database), pool_pre_ping=True)
        if env == 'test':
            Base.metadate.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns dictionary of all present object"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = nametoclass.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in nametoclass.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """Reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """Creates a new object"""
        self.__session.add(obj)

    def save(self):
        """Saves current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)
