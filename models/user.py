"""User model that inherits the base model"""

from models.base_model import BaseModel


class User(BaseModel):
    """creates new user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
