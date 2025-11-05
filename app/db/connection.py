import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ai_assistant_database.db")

def get_connection():
    """Создает и возвращает соединение с базой данных"""
    return sqlite3.connect(DB_PATH)

def get_connection_with_row_factory():
    """Создает и возвращает соединение с базой данных с поддержкой именованных столбцов"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn