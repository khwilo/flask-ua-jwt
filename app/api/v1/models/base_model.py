"""Base model definitions"""
from psycopg2.extras import RealDictCursor

from app.api.v1.models.queries import find_user_by_value
from manage import establish_connection


class BaseModel:
    """Definitions for the base model"""
    def __init__(self):
        self.connection = establish_connection()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def search_user(self, column, value):
        """Fetch a user from the 'users' table"""
        query = find_user_by_value(column, value)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
