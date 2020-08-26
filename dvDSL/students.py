import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE studenti (
            id SERIAL PRIMARY KEY,
            Indeks VARCHAR(255) NOT NULL,
            Ime VARCHAR(255) NOT NULL,
            Prezime VARCHAR(255) NOT NULL,
            Bodovi INTEGER,
            Ocena INTEGER
        )
        """,
       )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(database="jsd", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_students_list(students_list):
    """ insert multiple students into the studenti table  """
    sql = "INSERT INTO studenti(Indeks, Ime, Prezime, Bodovi, Ocena) VALUES(%s, %s, %s, %s, %s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(database="jsd", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,students_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()

    insert_students_list([
    ('ra-1-2015', 'Mika', 'Mikic', 55, 6 ,),
    ('ra-2-2015', 'Pera', 'Peric', 65, 7, ),
    ('ra-3-2015', 'Jovan', 'Jovanovic', 75, 8, ),
    ('ra-4-2015', 'Neko', 'Neko', 80, 8, ),
    ])
