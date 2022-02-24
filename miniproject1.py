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


def insert_data():  # for INSERTs
    global conn, c
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
