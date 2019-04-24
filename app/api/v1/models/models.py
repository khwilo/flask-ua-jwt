"""Use entity module"""
from datetime import datetime

from app.api.v1.models.base_model import BaseModel
from app.api.v1.models.queries import insert_user_query


class UserModel(BaseModel):
    """Entity representation for a user"""
    def __init__(self, **kwargs):
        super().__init__()
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.registered = str(datetime.utcnow())

    def save(self):
        """Add a new user to the 'users' table"""
        query = insert_user_query().format(
            self.firstname,
            self.lastname,
            self.email,
            self.password
        )
        self.cursor.execute(query)
        self.connection.commit()
