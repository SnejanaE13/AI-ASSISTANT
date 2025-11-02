from data_base.connection import get_connection


def create_db():
    conn = get_connection()
    cursor = conn.cursor()

    # creating table User
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,  
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        second_name VARCHAR(30),
        role VARCHAR(20) NOT NULL,
        password_hash TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        email VARCHAR(50) NOT NULL
        );
    """)

    # creating table Prompts
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS Prompts (
           prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
           title VARCHAR(10),
           content TEXT,
           created_at DATETIME,
           is_active BOOLEAN
           );
       """)

    # creating table Session
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Session (
        session_id TEXT PRIMARY KEY,
        token TEXT,
        user_id INTEGER,
        created_at DATETIME,
        expires_at DATETIME,
        is_active BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
        );
    """)

    # creating table Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id TEXT,
        sender_type VARCHAR(10),
        content TEXT,
        timestamp DATETIME,
        prompt_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (session_id) REFERENCES Session(session_id),
        FOREIGN KEY (prompt_id) REFERENCES Prompts(prompt_id)
        );
    """)

    conn.commit()
    conn.close()

