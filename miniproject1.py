import sqlite3
from getpass import getpass     # make pwd invisible

conn = None
c = None

def connect(path):  # connect to db
    global conn, c
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    conn.commit()
    return


def interface():
    pwd = getpass()
    print(pwd)
    return


def drop_tables():  # for DROPs
    pass

def define_tables():    # for CREATES
    global conn, c
    moviePeople = '''
        create table moviePeople (
            pid		char(4),
            name		text,
            birthYear	int,
            primary key (pid)
        );
    '''
    c.execute(moviePeople)

    conn.commit()
    return


def insert_data():  # for INSERTs
    pass


def main():
    connect("./miniproject1.db")
    interface()
    # define_tables()

    conn.commit()
    conn.close()
    return


if __name__ == '__main__':
	main()
