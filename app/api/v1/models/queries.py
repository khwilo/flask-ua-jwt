"""Database queries definitions"""


def create_user_table_query():
    """SQL query to create the users table"""
    users = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    registered_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """

    return users


def insert_user_query():
    """SQL query to insert a user to the 'users' table"""
    insert_user = """INSERT INTO users(
    firstname, lastname, email, password) VALUES(
    '{}', '{}', '{}', '{}'
    )"""
    return insert_user


def find_user_by_value(column, value):
    """
    SQL query to search if a record already exists in the 'users' table
    """
    query = """SELECT * FROM users WHERE {}='{}';""".format(column, value)
    return query


def drop_user_table_query():
    """SQL query to drop the users table"""
    drop_users = "DROP TABLE IF EXISTS users CASCADE"
    return drop_users


def create_blacklist_tokens_table_query():
    """SQL query to create the blacklist tokens table"""
    blacklist_tokens = """CREATE TABLE IF NOT EXISTS blacklist_tokens(
    id SERIAL PRIMARY KEY,
    token VARCHAR(500) UNIQUE NOT NULL,
    blacklisted_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """
    return blacklist_tokens


def insert_blacklist_token_query():
    """SQL query to insert a blacklist token to the 'blacklist_tokens' table"""
    insert_blacklist_token = """INSERT INTO blacklist_tokens(
    token) VALUES('{}')"""
    return insert_blacklist_token
