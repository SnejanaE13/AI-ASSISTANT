import sqlite3


def get_connection():
    return sqlite3.connect("../ai_assistant_database.db")