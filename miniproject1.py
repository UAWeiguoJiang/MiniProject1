import sqlite3
import sys
from getpass import getpass     # make pwd invisible

conn = None
c = None

def connect():  # connect to db
    global conn, c

    path = sys.argv[1]  # acquire database path from command line argument

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    conn.commit()
    return


def interface():
    global conn, c
    while True:
        options = input('Would you like to login, register or exit? (L / R / X): ')     # homepage

        if options.upper() == 'L':  # login
            while True:
                role = input('Would you like to login as a customer or an editor? (C / E): ')

                if role.upper() == 'C':     # login as customer
                    cid = input('cid: ')
                    pwd = getpass()     # invisible pwd
                    c.execute('select * from customers where cid = ? and pwd = ?;', (cid, pwd,))
                    validate = c.fetchall()
                    if validate == []:      # error checking, cid not in customers
                        print('Invalid cid or pwd, please try again!')
                    else:
                        customer(cid, pwd)  # perform operations as a customer
                        break
                elif role.upper() == 'E':   # login as editor
                    eid = input('eid: ')
                    pwd = getpass()     # invisible pwd
                    c.execute('select * from editors where eid = ? and pwd = ?;', (eid, pwd,))
                    validate = c.fetchall()
                    if validate == []:      # error checking, eid not in editors
                        print('Invalid eid or pwd, please try again!')
                    else:
                        editor(eid, pwd)    # perform operations as an editor
                        break
                else:
                    print('No such role, please try again!')

        elif options.upper() == 'R':       # registration
            while True:
                cid = input('cid: ')
                c.execute('select * from customers where cid = ?;', (cid,))
                validate = c.fetchall()
                if validate != []:  # error checking, cid already exists
                    print('cid already registered, please try a new one.')
                else:
                    break
            name = input('Name: ')
            pwd = getpass()
            c.execute('insert into customers values(?, ?, ?);', (cid, name, pwd,))
            print('Registration successful!')

        elif options.upper() == 'X':    # exit program
            break

        else:   # error checking, input other than L / R / X
            print('No such option!')

    conn.commit()
    return

def customer(cid, pwd):
    pass

def editor(eid, pwd):
    pass

def main():
    connect()
    interface()

    conn.commit()
    conn.close()
    return


if __name__ == '__main__':
	main()
