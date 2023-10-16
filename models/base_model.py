#!/usr/bin/python3

"""
Description of module: This is a module which contains the base model class.
"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel():
    """
    class:
        BaseModel

    attribute:
        1.id: string - assign with an uuid when an instance is created
        2.created_at: assign with the current datetime created
        3.updated_at: datetime - updated every time you change your object
    methods:
        1.save: updates the public instance attribute current datetime.
        2.to_dict: returns a dictionary containing all keys.
        3. Args:
            *args: Unused
            **Kwargs: Key/value pairs of attributes.
    """
    def __init__(self, *args, **kwargs):

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)


    def __str__(self):
        classname = "[{}] ".format(self.__class__.__name__)
        id = "({}) ".format(self.id)
        dict = "{}".format(self.__dict__)
        return classname + id + dict

    def save(self):
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Description: a dictionary representation of BaseModel.

        Returns:
            dict: Dictionary containing all keys/values of
                  __dict__ .
                  the __class__ key with the class name.
                  The created_at and updated_at attributes are converted
                  to string objects in ISO format.
        """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        return my_dict
