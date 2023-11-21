from datetime import datetime
import sqlite3

class DataBase():
    def __init__(self, db_path:str):
        self.db_path = db_path

    def create(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                datetime TEXT NOT NULL,
                user_id INTEGER,
                command TEXT,
                error TEXT
            )
        ''')

        connection.commit()
        connection.close()

    def add_command(self, uid:int, command:str, error:None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO commands (datetime, user_id, command, error) VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), uid, command, error))

        connection.commit()
        connection.close()