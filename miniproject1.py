import sqlite3
import sys
from getpass import getpass     # make pwd invisible
import datetime     # keep time

conn = None
c = None

def connect():  # connect to db
    """
        Function: connect() is a function that accepts the database's path as an argument from command line,
                  it connects to the database based on the path. Then it creates a global cursor object and
                  enforces foreign key constraint.

        Arguments: None

        Return: None
    """
    global conn, c

    path = sys.argv[1]  # acquire database path from command line argument

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    conn.commit()
    return


def interface():
    """
        Function: Login screen, provide options for both customers and editors to login. Both class of users
                  should be able to login using a valid id (respectively denoted as cid and eid for customers
                  and editors) and a password, denoted with pwd. Unregistered customers will be able to sign
                  up by providing a unique cid and additionally a name, and a password. Users will be able to
                  logout, which directs them to the first screen of the system. There is also an option to exit
                  the program directly. All calls to menus for customers and editors are made in this function
        
        Arguments: None

        Return: None
    """
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
                    print('Invalid option, please try again!')

        elif options.upper() == 'R':       # registration, case insensitive
            while True:
                cid = input('cid: ')
                c.execute('select * from customers where cid = ?;', (cid,))
                if c.fetchall() != []:  # error checking, cid already exists
                    print('cid already registered, please try a new one!')
                else:
                    break
            name = input('Name: ')
            pwd = getpass()
            c.execute('insert into customers values(?, ?, ?);', (cid, name, pwd,))
            print('Registration successful!')

        elif options.upper() == 'X':    # exit program, case insensitive
            break

        else:   # error checking, input other than L / R / X
            print('Invalid option, please try again!')

    conn.commit()
    return

def editor(eid, pwd):
    """
        Function: Menu for editor where editors can choose to add a movie or update recommendation.

        Arguments:
            eid: editor id
            pwd: editor's password
        
        Return: None
    """
    global c, conn

    while True:
        op = input('Would you like to add a movie, update a recommendation or logout? (A / U / L): ')
        if op.upper() == 'A':   # add a movie, case insensitive
            addMovie()
        elif op.upper() == 'U':     # update a recommendation, case insensitive
            updateRecommendation()
        elif op.upper() == 'L':     # logout, case insensitive
            break
        else:   # error checking
            print('Invalid option, please try again!')
    
    conn.commit()
    return


def addMovie():
    """
        Function: The editor will be able to add a movie by providing a unique movie id,
                  a title, a year, a runtime and a list of cast members and their roles. To add a
                  cast member, the editor needs to enter the id of the cast member, and the program
                  will look up the member and will display the name and the birth year. The editor
                  can confirm and provide the cast member role or reject the cast member. If the cast
                  member does not exist, the editor will be able to add the member by providing a
                  unique id, a name and a birth year.

        Argument: None

        Return: None
    """
    global c, conn

    while True:
        while True:
            mid = input('Please provide a movie id: ') # mid is an integer
            if mid.isnumeric() == True:
                break
            else:
                print("Movie id non-numerical, please try again!")
        c.execute('select * from movies where mid = ?;', (int(mid),))
        if c.fetchall() != []:      # if mid already exists
            print('mid already exists, please try a new one!')
        else:
            break   # keeps on asking for more info
    title = input('Title: ')
    while True:
        year = input('Year: ')     # year is an integer
        if year.isnumeric() == True:
            break
        else:
            print('Year non-integer, please try again!')
    while True:
        runtime = input('Runtime: ')   # runtime is an integer
        if runtime.isnumeric() == True:
            break
        else:
            print('Runtime non-integer, please try again!')
    c.execute('insert into movies values(?, ?, ?, ?);', (mid, title, int(year), int(runtime),))    # insert the new movie

    while True:
        addCasts = input('Insertion of new movie successful, would you like to proceed on adding casts? (Y / N) ')
        if addCasts.upper() == 'N':     # no casts added to this movie, case insensitive
            break
        
        elif addCasts.upper() == 'Y':   # start adding casts, case insensitive
            cnt = 1
            while True:
                print('cast{}'.format(cnt))     # keep track of casts, easier for debugging and better visualization
                pid = input('pid: ')    # pid case insensitive
                c.execute('''select DISTINCT m.name, m.birthYear
                            from moviePeople m, casts c
                            where m.pid = c.pid
                            and upper(m.pid) = ?;''', (pid.upper(),)) # find name and birth year
                nameAndBirth = c.fetchall()
                if nameAndBirth != []:  # if pid already exists, we display the name and the birth year
                    print(nameAndBirth[0][0] + ' ' + str(nameAndBirth[0][1]))   # convert birthYear to str for concatenation

                    while True:
                        confirm = input('Confirm and provide role or reject this cast? (C / R) ')
                        if confirm.upper() == 'C':  # confirm and provide role, case insensitive
                            role = input('Please provide the role of this cast in the movie: ')
                            c.execute('insert into casts values(?, ?, ?);', (mid, pid, role,))
                            break
                        elif confirm.upper() == 'R':    # reject cast, case insensitive
                            break
                        else:   # error checking
                            print('Invalid option, please try again!')
                else:   # if pid DNE, we add it
                    while True:
                        confirm = input('Cast member DNE and you can add it, do you want to proceed or reject? (P / R) ')
                        if confirm.upper() == 'P':  # add cast member, case insensitive
                            while True:     # ask editor to give a unique pid
                                pid = input('Please enter an unique pid: ')
                                c.execute('select * from moviePeople where upper(pid) = ?', (pid.upper(),))     # pid case insensitive
                                if c.fetchall() == []:  # check pid's uniqueness
                                    break
                                else:
                                    print('The pid provided is not unique, please try again.')

                            name = input('name: ')  # ask for additional info
                            while True:
                                birthYear = input('birth year: ')  # birthYear is an integer
                                if birthYear.isnumeric() == True:
                                    break
                                else:
                                    print('birthYear non-integer, please try again!')
                            c.execute('insert into moviePeople values(?, ?, ?);', (pid, name, int(birthYear),))

                            while True:
                                confirm2 = input('New member added successfully, confirm and provide role or reject this cast? (C / R) ')
                                if confirm2.upper() == 'C':     # provide role, case insensitive
                                    role = input('Please provide the role of this cast in the movie: ')
                                    c.execute('insert into casts values(?, ?, ?);', (mid, pid, role,))  # add to cast
                                    break
                                elif confirm2.upper() == 'R':   # reject role, case insensitive
                                    break
                                else:   # error checking
                                    print('Invalid option, please try again!')
                            break

                        elif confirm.upper() == 'R':    # reject adding cast member, case insensitive
                            break
                        else:   # error checking
                            print('Invalid option, please try again!')

                flag = False
                while True:     # ask editor to add another cast or not
                    add = input('Would you like to keep adding casts? (Y / N) ')
                    if add.upper() == 'Y':      # add another, case insensitive
                        cnt += 1
                        break
                    elif add.upper() == 'N':    # stop adding and set flag to break, case insensitive
                        flag = True
                        break
                    else:   # error checking
                        print('Invalid option, please try again!')
                if flag:
                    break
            break
        
        else:   # error checking
            print('Invalid option, please try again!')

    conn.commit()
    return


def updateRecommendation():
    """
        Function: The editor will be able to select a monthly, an annual or an all-time report
                  and see a listing of movie pairs m1, m2 such that some of the customers who
                  have watched m1, have also watched m2 within the chosen period. Any such pair
                  will be listed with the number of customers who have watched them within the
                  chosen period, ordered from the largest to the smallest number, and with an
                  indicator if the pair is in the recommended list and the score. A subroutine
                  updates() is called for following operations.
        
        Arguments: None

        Return: None
    """
    global c, conn

    while True:
        op = input('Would you like to see the monthly report, annual report, or all-time report? (M / A / AT) ')
        if op.upper() == 'AT':      # all-time report, case insensitive
            while True:
                print('ALL-TIME REPORT'.center(50))     # title
                print('pair #    watched 1    watched 2    count    score')     # auxiliary column names for better visualization
                c.execute('''
                            select t.mid1, t.mid2, t.cnt, ifnull(r.score, 'N/A')
                            from (select m1.mid as mid1, m2.mid as mid2, count(distinct c.cid) as cnt
                            from movies m1, watch w1, sessions s1, customers c, sessions s2, watch w2, movies m2
                            where m1.mid = w1.mid
                            and m1.runtime <= w1.duration * 2
                            and w1.sid = s1.sid
                            and s1.cid = c.cid
                            and c.cid = s2.cid
                            and s2.sid = w2.sid
                            and w2.mid = m2.mid
                            and w2.duration * 2 >= m2.runtime
                            and m2.mid != m1.mid
                            group by m1.mid, m2.mid
                            order by count(distinct c.cid) desc) as t left join recommendations r
                            on r.watched = t.mid1 and r.recommended = t.mid2;
                        ''')
                dictionary = dict()     # create a dict() to store each row in the report
                cnt = 1     # keep count of rows, used for row selection later
                for i in c.fetchall():
                    print('{:>3} {:>10} {:>13} {:>10} {:>9}'.format(str(cnt), str(i[0]), str(i[1]), str(i[2]), str(i[3])))
                    dictionary[str(cnt)] = [i[0], i[1], i[2], i[3]]
                    cnt += 1
                print('* N/A means the pair is not in recommendations.')
                updates(dictionary)     # proceed to perform operations the editor desires
                flag = False
                while True:
                    op = input('Would you like to work on a new pair or stop updating recommendations? (N / S) ')
                    if op.upper() == 'N':   # keep updating, case insensitive
                        break
                    elif op.upper() == 'S': # stop updating, case insensitive
                        flag = True
                        break
                    else:   # error checking
                        print('Invalid option, please try again!')
                if flag:
                    break
            break

        elif op.upper() == 'A':     # annual report, case insensitive
            while True:
                print('ANNUAL REPORT'.center(50))
                print('pair #    watched 1    watched 2    count    score')
                c.execute('''
                            select t.mid1, t.mid2, t.cnt, ifnull(r.score, 'N/A')
                            from (select m1.mid as mid1, m2.mid as mid2, count(distinct c.cid) as cnt
                            from movies m1, watch w1, sessions s1, customers c, sessions s2, watch w2, movies m2
                            where m1.mid = w1.mid
                            and m1.runtime <= w1.duration * 2
                            and w1.sid = s1.sid
                            and s1.cid = c.cid
                            and c.cid = s2.cid
                            and s2.sid = w2.sid
                            and w2.mid = m2.mid
                            and w2.duration * 2 >= m2.runtime
                            and m2.mid != m1.mid
                            and s1.sdate >= date('now', '-365 days')
                            and s2.sdate >= date('now', '-365 days')
                            group by m1.mid, m2.mid
                            order by count(distinct c.cid) desc) as t left join recommendations r
                            on r.watched = t.mid1 and r.recommended = t.mid2;
                    ''')
                dictionary = dict()
                cnt = 1
                for i in c.fetchall():
                    print('{:>3} {:>10} {:>13} {:>10} {:>9}'.format(str(cnt), str(i[0]), str(i[1]), str(i[2]), str(i[3])))
                    dictionary[str(cnt)] = [i[0], i[1], i[2], i[3]]
                    cnt += 1
                print('* N/A means the pair is not in recommendations.')
                updates(dictionary)
                flag = False
                while True:
                    op = input('Would you like to work on a new pair or stop updating recommendations? (N / S) ')
                    if op.upper() == 'N':   # keep updating, case insensitive
                        break
                    elif op.upper() == 'S': # stop updating, case insensitive
                        flag = True
                        break
                    else:   # error checking
                        print('Invalid option, please try again!')
                if flag:
                    break
            break

        elif op.upper() == 'M':     # monthly report, case insensitive
            while True:
                print('MONTHLY REPORT'.center(50))
                print('pair #    watched 1    watched 2    count    score')
                c.execute('''
                    select t.mid1, t.mid2, t.cnt, ifnull(r.score, 'N/A')
                    from (select m1.mid as mid1, m2.mid as mid2, count(distinct c.cid) as cnt
                        from movies m1, watch w1, sessions s1, customers c, sessions s2, watch w2, movies m2
                        where m1.mid = w1.mid
                        and m1.runtime <= w1.duration * 2
                        and w1.sid = s1.sid
                        and s1.cid = c.cid
                        and c.cid = s2.cid
                        and s2.sid = w2.sid
                        and w2.mid = m2.mid
                        and w2.duration * 2 >= m2.runtime
                        and m2.mid != m1.mid
                        and s1.sdate >= date('now', '-30 days')
                        and s2.sdate >= date('now', '-30 days')
                        group by m1.mid, m2.mid
                        order by count(distinct c.cid) desc) as t left join recommendations r
                        on r.watched = t.mid1 and r.recommended = t.mid2;
                    ''')
                dictionary = dict()
                cnt = 1
                for i in c.fetchall():
                    print('{:>3} {:>10} {:>13} {:>10} {:>9}'.format(str(cnt), str(i[0]), str(i[1]), str(i[2]), str(i[3])))
                    dictionary[str(cnt)] = [i[0], i[1], i[2], i[3]]
                    cnt += 1
                print('* N/A means the pair is not in recommendations.')
                updates(dictionary)
                flag = False
                while True:
                    op = input('Would you like to work on a new pair or stop updating recommendations? (N / S) ')
                    if op.upper() == 'N':   # keep updating, case insensitive
                        break
                    elif op.upper() == 'S': # stop updating, case insensitive
                        flag = True
                        break
                    else:   # error checking
                        print('Invalid option, please try again!')
                if flag:
                    break
            break

        else:   # error checking
            print('Invalid option, please try again!')

    conn.commit()
    return


def updates(dictionary):
    """
        Function: The editor will be able to select a pair and (1) add it to the recommended list (if not
                  there already) or update its score, or (2) delete a pair from the recommended list.
        
        Arguments: None

        Return: None
    """
    while True:     # get pair #
        choosePair = input('Please choose a pair #: ')
        if choosePair not in dictionary.keys():     # error checking for invalid pair #
            print('Invalid pair #, please try again!')
        else:
            pair = dictionary[choosePair]
            mid1 = pair[0]  # find mids of the pair
            mid2 = pair[1]
            c.execute('select * from recommendations r where r.watched = ? and r.recommended = ?;', (mid1, mid2,))
            if c.fetchall() == []:      # if the pair DNE in recommendations
                while True:
                    op = input('The pair you choose DNE, would you like to add it to recommendations? (Y / N) ')
                    if op.upper() == 'N':   # case insensitive
                        break
                    elif op.upper() == 'Y': # case insensitive
                        while True:
                            score = input('Please provide a score: ')
                            if score.isnumeric() == False and isFloat(score) == False:   # if it's neither an integer or a float
                                print('Score non-numerical, please try again!')
                            else:
                                c.execute('insert into recommendations values(?, ?, ?);', (mid1, mid2, float(score),))
                                print('Insertion successful, a new report is generated!')
                                break
                        break
                    else:   # error checking
                        print('Invalid option, please try again!')
            else:   # if the pair exists in recommendations
                while True:
                    op = input('The pair you choose exists, would you like to update its score or delete it? (U / D) ' )
                    if op.upper() == 'U':   # update score, case insensitive
                        while True:
                            score = input('Please provide a score: ')
                            if score.isnumeric() == False and isFloat(score) == False:
                                print('Score non-numerical, please try again!')
                            else:
                                c.execute('update recommendations set score = ? where watched = ? and recommended = ?;', (float(score), mid1, mid2,))
                                print('Update successful!')
                                break
                        break
                    elif op.upper() == 'D': # delete score, case insensitive
                        c.execute('delete from recommendations where watched = ? and recommended = ?;', (mid1, mid2,))
                        print('Deletion successful, a new report is generated!')
                        break
                    else:
                        print('Invalid option, please try again!')
                break
    
        conn.commit()
        return


def isFloat(f):
    """
        Function: check if an input string can be converted to float or not, used
                  for error checking.

        Argument:
            f: input string to be converted
        
        Return: True if the str can be converted to float, False otherwise.
    """
    try:
        float(f)
        return True
    except ValueError:
        return False


def customer(cid, pwd):
    pass


def searchMovies(cid):
    # customer can search for movie by providing keywords
    # cid is the customers' id
    
    global startTime, SID, conn, c
    
    # handling keywords
    keywordsList = []
    while (keywordsList ==[]):
        keywords = input('Enter Keywords: ').strip() # get keywords from user without '/n' charater
        keywordsList = keywords.split(); # split the keywords by a space
    for i in range(len(keywordsList)):
        keywordsList[i] = '%'+keywordsList[i].upper()+'%' # turn the terms into "%?%" form
    
    # new keyword list for the subqueries because we want to check for cast name, movie title and cast role
    newKeywordList = []
    for word in keywordsList:
        for i in range(3):
            newKeywordList.append(word)
    
    # creating place holder for the subqueries
    subqueries = "UNION ALL".join([" SELECT DISTINCT(m.mid), m.title, m.year, m.runtime FROM movies m, casts c, moviePeople mp WHERE m.mid = c.mid AND c.pid = mp.pid AND (m.title LIKE ? OR c.role like ? OR mp.name like ?) "
                                   for words in keywordsList])
    # execute the queries
    c.execute(f'''SELECT * FROM ({subqueries}) GROUP BY mid ORDER BY COUNT(title) DESC;''', newKeywordList);
    moviesList = c.fetchall()
    
    if (moviesList == []):
        print('NO RESULT... RETURNING TO MAIN MENU...')
        return
    
    #print(moviesList)
    
    moviesListStartIndex = 0 #first position of movies to be printed
    moviesListEndIndex = 5 #stop printing at this position
    
    while True:
        print('0 -- Display more movies')
        
        # make sure there is enough movie to print
        if (moviesListEndIndex > len(moviesList)):
            moviesListEndIndex = len(moviesList)
        
        # make sure there is something to display
        if (moviesListEndIndex <= moviesListStartIndex):
            moviesListStartIndex = moviesListEndIndex - 5
        
        # make sure start index is positive
        if (moviesListStartIndex < 0):
            moviesListStartIndex = 0
        
        for i in range(moviesListStartIndex, moviesListEndIndex):
            print(str(i+1) + ' -- TITLE: ' + moviesList[i][1] + ', YEAR: ' + str(moviesList[i][2]) + ', RUNTIME: ' + str(moviesList[i][3]))
        
        action = input('Enter selection: ')
        
        # make sure user enters integer type of input
        try:
            action = int(action)
        except:
            print("Please enter numeric inputs...")
        
        # display more movies 
        if (action == 0): 
            moviesListStartIndex = moviesListEndIndex
            moviesListEndIndex += 5
        
        # selecting a specific
        else:
            # make sure selection is in the list
            try:
                selectedMovie = moviesList[action-1]
            except:
                print('Please choose within the range...')
            else:
                break
    
    # find casts of the customer selected movies
    movieID = selectedMovie[0]
    c.execute('SELECT mp.pid, mp.name FROM moviePeople mp, casts c WHERE c.pid = mp.pid AND c.mid=:ID;', {'ID':movieID})
    casts = c.fetchall()
    
    # find number of customer watched the movie
    c.execute('SELECT m.mid, count(distinct cid) FROM movies m, watch w WHERE m.mid = w.mid AND w.mid=:ID AND w.duration >= 0.5*m.runtime GROUP BY m.mid;', {'ID': movieID})
    counts = c.fetchall()
    
    if (counts == []):
        count = 0
    else:
        count = counts[0][1]
    
    # print the movie
    print('TITLE: ' + selectedMovie[1] + ', YEAR: ' + str(selectedMovie[2]) + ', RUNTIME: ' + str(selectedMovie[3]))
    # print the casts
    for i in range(len(casts)):
        print(chr(9) + 'Cast ' + str(i+1) + ': ' + casts[i][1])
    # print number of customer watched the movie
    print(chr(9) + 'Number of Watches: ' + str(count))
    
    # prompt for selection to either follow cast or watch movie
    while True:
        print('0 -- Start watching')
        print('Select a casts from below to follow')
        
        for i in range(len(casts)):
            print(chr(9) + str(i+1) + ' -- ' + casts[i][1])        
        
        selection = input('Selection: ')
        # make sure user enters integer type of input
        try:
            selection = int(selection)
        except:
            print("Please enter numeric inputs...")    
        
        # start watching a movie
        if (selection == 0):
            # handle if no sessions available
            if (SID == None):
                print('No available sessions... Returning to main menu...')
                break
            
            else:
                c.execute('SELECT * FROM sessions WHERE cid=:CID AND sid=:SID;', {'CID':cid, 'SID': SID})
                sessions = c.fetchall()
                if (sessions == []): # make sure the session is started
                    print('No available sessions... Returning to main menu...')
                    break
                else:
                    # inserting into watch table
                    try:
                        c.execute('INSERT INTO watch VALUES (?,?,?,?);', (SID, cid, movieID, 0))
                    except:
                        print('Already have a session... Returning to main menu...')
                        break
                    else:
                        conn.commit()
                        startTime = datetime.datetime.now()  # keep track of the time                                   
                        print('Successfully started to watch a movie! Returning to main menu...')
                        break
        
        # makes sure selection is within the range of casts
        try:
            selectedCast = casts[selection-1]
        except:
            print('Please choose within the range...')
        else:
            try:
                c.execute('INSERT INTO follows VALUES(?,?);', (cid, selectedCast[0]))
            except:
                print('Already following the cast... Returning to main menu...')
                break
            else:
                print('Successfully followed a cast... Returning to main menu...')
                conn.commit()
            break
    return

def endWatchingMovie(cid):
    # end a watching movie started during the same log in
    # assumption: customer can only watch one movie
    #     - by choosing this option, the system automatically end a movie
    #       if there is any outstanding watching movies
    # cid is the cid from customer table
    
    global startTime, SID, conn, c
    
    # check if there is a session
    if (SID == None):
        print('No available sessions... Returning to main menu...')
        return
    
    # check if there is a session
    else:
        c.execute('SELECT * FROM sessions WHERE cid=:CID AND sid=:SID;', {'CID':cid, 'SID': SID})
        sessions = c.fetchall()
        if (sessions == []): # make sure the session is started
            print('No available sessions... Returning to main menu...')
            return
    
    if (startTime == None):
        print('Not watching any movies... Returning to main menu...')
        return
    
    diff = datetime.datetime.now() - startTime #get the time difference
    
    newDuration = round(diff.total_seconds() / 60) # get duration to the nearest minutes
    
    # get the runtime of the movie
    c.execute('SELECT m.runtime FROM movies m, watch w WHERE m.mid = w.mid AND w.cid=:CID AND w.sid =:SID;', {'CID':cid, 'SID':SID})
    runtime = c.fetchall()
    if (runtime == None):
        print("Not watching any movies... Returning to main menu...")
        return
    else: # checks if newDuration is greater than runtime
        if (newDuration > runtime[0][0]):
            newDuration = runtime[0][0]
    
    # update the duration in watch table
    c.execute(f'''UPDATE watch SET duration = duration + ? WHERE cid = ? AND sid = ?;''', [newDuration, cid, SID])
    conn.commit()
    print('Sucessfully ended a move... Returning to main menu')
    startTime = None
    return


def main():
    connect()
    interface()

    conn.commit()
    conn.close()
    return


if __name__ == '__main__':
	main()
