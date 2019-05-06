"""Module for the database specific operations"""
import os
from os.path import join, dirname

import psycopg2

from dotenv import load_dotenv

from flask import current_app

from app.api.v1.models.queries import create_user_table_query, \
    drop_user_table_query, create_blacklist_tokens_table_query

DOTENV_PATH = join(dirname(__file__), ".env")

load_dotenv(DOTENV_PATH)


def establish_connection():
    """Establish a database connection"""
    database_url = current_app.config["DATABASE_URL"]
    try:
        connection = psycopg2.connect(database_url)
    except psycopg2.DatabaseError as error:
        print("error {}".format(error))
    return connection


def create_table(connection):
    """Create a database table"""
    cursor = connection.cursor()
    queries = [
        create_user_table_query(), create_blacklist_tokens_table_query()
    ]
    for query in queries:
        cursor.execute(query)
        connection.commit()


def destroy(database_url):
    """Drop a database table"""
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    query = drop_user_table_query()
    cursor.execute(query)
    connection.commit()


def migrate(database_url):
    """Create the users table"""
    connection = psycopg2.connect(database_url)
    create_table(connection)


def migrate_dev():
    """Perform database migrations for the development environment database"""
    migrate(os.getenv("DATABASE_URL"))


def migrate_test():
    """Perform database migrations for the test environment database"""
    migrate(os.getenv("DATABASE_TEST_URL"))


def drop_dev():
    """Drop the development environment database table"""
    destroy(os.getenv("DATABASE_URL"))

if __name__ == "__main__":
    drop_dev()
    migrate_dev()
