import psycopg2
import utils

conn = psycopg2.connect(database='my_db',
                        user='postgres',
                        password='Mer1',
                        host='localhost',
                        port=5432)

cur = conn.cursor()

create_users_table = """DROP TABLE IF EXISTS users CASCADE;
    CREATE TABLE users(
        id serial PRIMARY KEY ,
        username VARCHAR(100) NOT NULL UNIQUE ,
        password VARCHAR(255) NOT NULL ,
        role VARCHAR(20) NOT NULL ,
        status VARCHAR(30) NOT NULL ,
        login_try_count INT NOT NULL 
    );
"""

create_todos_table = """DROP TABLE IF EXISTS todos;
    CREATE TABLE IF NOT EXISTS todos(
        id serial PRIMARY KEY ,
        name VARCHAR(100) NOT NULL ,
        todo_type VARCHAR(15) NOT NULL ,
        user_id INT REFERENCES users(id)
    );
"""


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        conn.commit()
        return result

    return wrapper


def create_table():
    cur.execute(create_users_table)
    cur.execute(create_todos_table)
    conn.commit()


@commit
def migrate():
    insert_into_users = """
    insert into users (username, password, role, status,login_try_count) 
    values (%s,%s,%s,%s,%s);
    """
    data = ('admin', utils.hash_password('123'), 'ADMIN', 'ACTIVE', 0)
    cur.execute(insert_into_users, data)


@commit
def init():
    create_table()
    migrate()


init()
