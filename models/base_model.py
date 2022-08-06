#!/usr/bin/pyhon3
""" Base class for modelling subclasses"""
from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    """ Defines common attributes and methods for all other objects """
    def __init__(self, *args, **kwargs):
        """ Initialize a class instance """
        if kwargs:
            fmt = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(kwargs[key], fmt)
                if key != '__class__':
                    setattr(self, key, value)  
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """ Returns string representation of an instance """
        rep = "[{0}] ({1}) {2}".format(self.__class__.__name__, self.id,
                                       self.__dict__)
        return rep

    def save(self):
        """ Updates last update time """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns a dictionary of all instance attributes """
        new_dict = {}

        for key, values in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                new_dict[key] = values.strftime("%Y-%m-%dT%H:%M:%S.%f")
            else:
                if not values:
                    pass
                else:
                    new_dict[key] = values
        new_dict['__class__'] = self.__class__.__name__

        return new_dict
