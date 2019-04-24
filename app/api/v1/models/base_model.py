"""Base model definitions"""
from psycopg2.extras import RealDictCursor

from manage import establish_connection


class BaseModel:
    """Definitions for the base model"""
    def __init__(self):
        self.connection = establish_connection()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
