#!/usr/bin/python3

""" This module contains the console for the AirBnB clone"""

import cmd
from models.user import User
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models.engine.file_storage import FileStorage
from json import dumps
import ast


class HBNBCommand(cmd.Cmd):
    """
    This is the entry point for the command interpreter
    """

    prompt = '(hbnb) '
    models = {
        'BaseModel': BaseModel,
        'User': User,
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State
    }

    def do_quit(self, args):

        """
        Quits the program
        """
        raise SystemExit

    def do_EOF(self, args):

        """
        Exit after receiving EOF signal
        """
        print()
        return True

    def emptyline(self):
        """
        An empty line and ENTER does nothing
        """
        pass

    def do_help(self, args):
        """
        Provides a list of all available commands.
        """
        cmd.Cmd.do_help(self, args)

    def do_create(self, args):
        """creates new instances of BaseModel class and
        saves it to a Json.
        """

        if not (args):
            print("** class name missing **")
            return
        if (args in self.models.keys()):
            instance = eval(args)()
            instance.save()
            print(instance.id)
            return
        print("** class doesn't exist **")

    def do_show(self, args):
        """
        shows spring representation of an instance
        """

        instances = FileStorage()
        instances.reload()
        if (len(args) == 0):
            print("** class name missing **")
            return
        tofind = args.split(' ')
        if (tofind[0] not in self.models):
            print("** class doesn't exist **")
            return
        if (len(tofind) == 1):
            print("** instance id missing **")
            return
        for identifier in list(instances.all()):
            id = identifier.split('.')
            if (id[0] == tofind[0] and id[1] == tofind[1]):

                print(str(instances.all()[identifier]))
                return
        print("** no instance found **")

    def do_destroy(self, args):
        """
        deletes an instance on the basis of class and id name
        """
        instances = FileStorage()
        instances.reload()
        if (len(args) == 0):
            print("** class name missing **")
            return
        tofind = args.split(' ')
        if (tofind[0] not in self.models.keys()):
            print("** class doesn't exist **")
            return
        if (len(tofind) == 1):
            print("** instance id missing **")
            return
        for identifier in list(instances.all()):
            id = identifier.split('.')
            if (id[0] == tofind[0] and id[1] == tofind[1]):
                instances.all().pop(identifier)
                instances.save()
                return
        print("** no instance found **")

    def do_all(self, args):
        """
        shows all instances of string representation
        """

        instances = FileStorage()
        instances.reload()
        result = []
        if (len(args) == 0):
            for identifier in list(instances.all()):
                splitID = identifier.split('.')
                if (splitID[0] in self.models.keys()):
                    dict = eval(
                        splitID[0])(
                        **instances.all()[identifier].to_dict())
                    result.append(
                        str(dict))

        else:
            tofind = args.split(' ')
            if (tofind[0] not in self.models):
                print("** class doesn't exist **")
                return

            for identifier in list(instances.all()):
                id = identifier.split('.')
                if (id[0] == tofind[0]):
                    result.append(
                        str(instances.all()[identifier])
                    )
        print(result)

    def do_update(self, args):
        """
        update instances on the basis of  id name
        """
        instances = FileStorage()
        instances.reload()
        if (len(args) == 0):
            print("** class name missing **")
            return
        tofind = args.split(' ')
        if (tofind[0] not in self.models):
            print("** class doesn't exist **")
            return
        if (len(tofind) == 1):
            print("** instance id missing **")
            return
        if (len(tofind) == 2):
            print("** attribute name missing **")
            return
        if (len(tofind) == 3):
            print("** value missing **")
            return
        for identifier in list(instances.all()):
            id = identifier.split('.')
            value = tofind[3].strip('"')

            if id[0] == tofind[0] and id[1] == tofind[1]:
                obj = instances.all()[identifier]

                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

                setattr(obj, tofind[2], value)
                instances.save()
                return

        print("** no instance found **")

    def default(self, line):
        """
        Takes all functions that are not properly defined
        """
        args = line.split('.')
        if len(args) != 2:
            print("** Unknown syntax: {}".format(line))
            return

        class_name, action = args[0], args[1].split('(')[0]
        action_args = args[1][len(action) + 1:-1]

        if class_name in self.models.keys():
            if action == "all":
                self.do_all(class_name)
            elif action == "count":
                self.do_count(class_name)
            elif action == "show":
                action_args = action_args.strip('"')
                self.do_show(f"{class_name} {action_args}")
            elif action == "destroy":
                action_args = action_args.strip('"')
                self.do_destroy(f"{class_name} {action_args}")
            elif action == "update":
                try:
                    if "{" in action_args:
                        id, update_dict_str = [
                            arg.strip(' "')
                            for arg in action_args.split(',', 1)
                        ]
                        update_dict = ast.literal_eval(update_dict_str)
                        update_command = f"{class_name} {id} {update_dict}"
                        self.do_update_dict(update_command)
                    else:
                        id, attribute_name, attribute_value = [
                            arg.strip(' "') for arg in action_args.split(',')
                        ]
                        update_command = (
                            f"{class_name} {id} "
                            f"{attribute_name} {attribute_value}"
                        )
                        self.do_update(update_command)
                except ValueError:
                    print("** Invalid syntax **")

    def do_update_dict(self, args):
        """
        Updates an instance based on its ID 
        """
        instances = FileStorage()
        instances.reload()
        args_list = args.split(' ', 2)
        class_name = args_list[0]
        instance_id = args_list[1]
        update_dict = eval(args_list[2])

        instance_key = f"{class_name}.{instance_id}"
        if instance_key not in instances.all():
            print("** no instance found **")
            return

        instance = instances.all()[instance_key]
        for key, value in update_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(instance, key, value)
        instance.save()

    def do_count(self, class_name):
        """
        Count the number of instances
        """
        instances = FileStorage()
        instances.reload()

        count = 0
        for identifier in list(instances.all()):
            id_split = identifier.split('.')
            if id_split[0] == class_name:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()    
