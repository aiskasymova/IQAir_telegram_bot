import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

class PostgresDb:

    def __init__(self):

        self.connection = psycopg2.connect(user="aisula",
                                           password="myPassword",
                                           host="localhost",
                                           port="5432",
                                           database="mydbase")
        self.cursor = self.connection.cursor()
        self.table = '''CREATE TABLE IF NOT EXISTS subscriptions(ID INT PRIMARY KEY NOT NULL, USER_ID INT NOT NULL,STATUS BOOL, CITY VARCHAR(128) NOT NULL); '''

        self.cursor.execute(self.table)

    def get_subscriptions(self, status=True):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT USER_ID, CITY FROM subscriptions WHERE STATUS = {status}")
            return cursor.fetchall()

    def subscriber_exists(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM subscriptions WHERE USER_ID = {user_id}')
            res = cursor.fetchall()
            # print(res)
            # print(bool(len(res)))
            return bool(len(res))

    def add_subscriber(self, user_id, city, status=True):
        with self.connection.cursor() as cursor:
            print("in Add subscr")
            cursor.execute("SELECT ID FROM subscriptions")
            rows = cursor.fetchall()
            id_tab = 1
            for row in rows:
                id_tab += 1
            return cursor.execute(
                f"INSERT INTO subscriptions (ID, USER_ID, STATUS, CITY) VALUES {(id_tab, user_id, status, city)}")

    def update_subscription(self, user_id, status):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE subscriptions SET STATUS = {status} WHERE USER_ID = {user_id}")

    def check_status(self, user_id):
        self.cursor.execute(
            f'SELECT STATUS FROM subscriptions WHERE USER_ID = {user_id}')
        status = self.cursor.fetchone()
        print(status)

        return str(status)

    def print_info(self):
        self.cursor.execute("SELECT * FROM subscriptions")
        rows = self.cursor.fetchall()
        for row in rows:
            print("ID", row[0])
            print("USER_ID", row[1])
            print("STATUS", row[2])

    def close(self):
        self.connection.close()
