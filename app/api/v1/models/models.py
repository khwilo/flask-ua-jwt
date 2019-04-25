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

    def find_user_by_email(self, value):
        """Find a user by his/her email address"""
        result = self.search_user("email", value)
        return result

    @staticmethod
    def to_json(result):
        """Return a JSON representation of the user's info"""
        return {
            "id": result["id"],
            "firstname": result["firstname"],
            "lastname": result["lastname"],
            "email": result["email"],
            "isAdmin": result["is_admin"],
            "registered": str(result["registered_on"]),
        }
