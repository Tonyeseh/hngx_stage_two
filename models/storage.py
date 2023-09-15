import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

db_name = os.environ.get("DB_NAME")
user_name = os.environ.get("DB_USER")
db_pwd = os.environ.get("DB_PWD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_url = os.environ.get("DATABASE_URL")


class Storage():
    """storage class for the app"""

    def __init__(self) -> None:
        self.conn = psycopg2.connect(db_url)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, name varchar);")

    def save(self) -> None:
        """saves the current session"""
        self.conn.commit()

    def close(self) -> None:
        """closes the current cursor open/transaction"""
        self.cur.close()
        self.conn.close()

    def create(self, name: str) -> bool:
        """creates a new record in the database"""
        self.cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        status = self.cur.statusmessage[-1]
        self.save()
        if status == "1":
            return True
        return False

    def get(self, id: int) -> dict:
        """gets info from the database"""
        self.cur.execute("SELECT * FROM users WHERE id=(%s)", (id,))
        status = self.cur.statusmessage[-1]
        self.save()
        if status == "1":
            res = self.cur.fetchone()
            return {res[0]: res[1]}
        return {}

    def update(self, id: int) -> dict:
        """updates a record in the database"""
        self.cur.execute("UPDATE users WHERE id=(%s)", (id,))
        status = self.cur.statusmessage[-1]
        self.save()
        if status == "1":
            return True
        return False

    def delete(self, id: int) -> bool:
        """deletes record in the db with id"""
        self.cur.execute("DELETE FROM users WHERE id=(%s)", (id,))
        status = self.cur.statusmessage[-1]
        self.save()
        if status == "1":
            return True
        return False
