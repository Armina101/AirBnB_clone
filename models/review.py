"""Review model for the base model"""

from models.base_model import BaseModel


class Review(BaseModel):
    """creates new review model"""
    place_id = ""
    user_id = ""
    text = ""
