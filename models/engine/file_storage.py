#!/usr/bin/python3

"""
FileStorage class handles storage and
reload of instances
"""
from json import loads, dump
from models.user import User
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from os.path import exists


class FileStorage:
    """Storage class, allows for CRUD operations on objects"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns all stored objects"""
        return self.__objects

    def new(self, obj):
        """Creates new object"""
        attr = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[attr] = obj

    def save(self):
        """Save objects to output.json"""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, "w") as f:
            dump(serialized_objects, f)

    def reload(self):
        """Reads from output.json to load objects"""
        current_classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'Review': Review,
            'State': State
        }
        if (exists(self.__file_path)):
            with open(self.__file_path, "r") as f:
                data = f.read()
            json_decode = loads(data)
            for key, value in json_decode.items():
                class_name = value['__class__']
                if class_name in current_classes:
                    self.__objects[key] = current_classes[class_name](**value)
