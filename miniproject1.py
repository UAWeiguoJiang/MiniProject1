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

                if role.upper() == 'C':     # login as customer, case insensitive
                    cid = input('cid: ')
                    pwd = getpass()     # invisible pwd
                    c.execute('select * from customers where cid = ? and pwd = ?;', (cid, pwd,))
                    if c.fetchall() == []:      # error checking, cid not in customers
                        print('Invalid cid or pwd, please try again!')
                    else:
                        customer(cid, pwd)  # perform operations as a customer
                        break
                elif role.upper() == 'E':   # login as editor, case insensitive
                    eid = input('eid: ')
                    pwd = getpass()     # invisible pwd
                    c.execute('select * from editors where eid = ? and pwd = ?;', (eid, pwd,))
                    if c.fetchall() == []:      # error checking, eid not in editors
                        print('Invalid eid or pwd, please try again!')
                    else:
                        editor(eid, pwd)    # perform operations as an editor
                        break
                else:
                    print('No such role, please try again!')

        elif options.upper() == 'R':       # registration, case insensitive
            while True:
                cid = input('cid: ')
                c.execute('select * from customers where cid = ?;', (cid,))
                if c.fetchall() != []:  # error checking, cid already exists
                    print('cid already registered, please try a new one.')
                else:
                    break
            name = input('Name: ')
            pwd = getpass()
            c.execute('insert into customers values(?, ?, ?);', (cid, name, pwd,))
            print('Registration successful!')

        elif options.upper() == 'X':    # exit program, case insensitive
            break

        else:   # error checking, input other than L / R / X
            print('No such option!')

    conn.commit()
    return

def customer(cid, pwd):
    pass

def editor(eid, pwd):
    global c, conn

    while True:
        op = input('Would you like to add a movie, update a recommendation or logout? (A / U / L): ')
        if op.upper() == 'A':
            addMovie()
        elif op.upper() == 'U':
            updateRecommendation()
        elif op.upper() == 'L':
            break
        else:
            print('No such option!')
    
    conn.commit()
    return

def addMovie():
    global c, conn

    while True:
        mid = int(input('Please provide a movie id: ')) # mid is an integer
        c.execute('select * from movies where mid = ?;', (mid,))
        if c.fetchall() != []:      # if mid already exists
            print('mid already exists, please try entering another one.')
        else:
            break   # keeps on asking for more info
    title = input('Title: ')
    year = int(input('Year: '))     # year is an integer
    runtime = int(input('Runtime: '))   # runtime is an integer
    c.execute('insert into movies values(?, ?, ?, ?);', (mid, title, year, runtime,))    # insert the new movie

    while True:
        addCasts = input('Insertion of new movie successful, would you like to proceed on adding casts? (Y / N) ')
        if addCasts.upper() == 'N':     # no casts added to this movie
            break
        
        elif addCasts.upper() == 'Y':   # start adding casts
            cnt = 1
            while True:
                print('cast{}'.format(cnt))     # keep track of casts, easier for debugging and better visualization
                pid = input('pid: ')
                c.execute('''select DISTINCT m.name, m.birthYear
                            from moviePeople m, casts c
                            where m.pid = c.pid
                            and m.pid = ?;''', (pid,)) # find name and birth year
                nameAndBirth = c.fetchall()
                if nameAndBirth != []:  # if pid already exists, we display the name and the birth year
                    print(nameAndBirth[0][0] + ' ' + str(nameAndBirth[0][1]))   # convert birthYear to str for concatenation

                    while True:
                        confirm = input('Confirm and provide role or reject this cast? (C / R) ')
                        if confirm.upper() == 'C':  # case insensitive
                            role = input('Please provide the role of this cast in the movie: ')
                            c.execute('insert into casts values(?, ?, ?);', (mid, pid, role,))
                            break
                        elif confirm.upper() == 'R':
                            break
                        else:
                            print('No such option!')
                else:
                    while True:
                        confirm = input('Cast member DNE and you can add it, do you want to proceed or reject? (P / R) ')
                        if confirm.upper() == 'P':
                            while True:     # ask editor to give a unique pid
                                pid = input('Please enter an unique pid: ')
                                c.execute('select * from moviePeople where pid = ?', (pid,))
                                if c.fetchall() == []:  # check pid's uniqueness
                                    break
                                else:
                                    print('The pid provided is not unique, please try again.')

                            name = input('name: ')  # ask for additional info
                            birthYear = int(input('birth year: '))
                            c.execute('insert into moviePeople values(?, ?, ?);', (pid, name, birthYear,))

                            while True:
                                confirm2 = input('New member added successfully, confirm and provide role or reject this cast? (C / R) ')
                                if confirm2.upper() == 'C':
                                    role = input('Please provide the role of this cast in the movie: ')
                                    c.execute('insert into casts values(?, ?, ?);', (mid, pid, role,))  # add to cast
                                    break
                                elif confirm2.upper() == 'R':
                                    break
                                else:
                                    print('No such option!')
                            break

                        elif confirm.upper() == 'R':
                            break
                        else:
                            print('No such option!')

                flag = False
                while True:
                    add = input('Would you like to keep adding casts? (Y / N) ')
                    if add.upper() == 'Y':
                        cnt += 1
                        break
                    elif add.upper() == 'N':
                        flag = True
                        break
                    else:
                        print('No such option!')
                if flag:
                    break
            break
        
        else:
            print('No such option!')

    conn.commit()
    return

def updateRecommendation():
    pass

def main():
    connect()
    interface()

    conn.commit()
    conn.close()
    return


if __name__ == '__main__':
	main()
