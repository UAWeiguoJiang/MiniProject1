import sqlite3

conn = None
c = None

def connect(path):
    global conn, c
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    conn.commit()
    return


def drop_tables():
    editors = "drop table if exists editors;"

    conn.commit()
    return


def define_tables():
    moviePeople = '''
    create table moviePeople (
        pid		char(4),
        name		text,
        birthYear	int,
        primary key (pid)
    );'''
    
    movies = '''
    create table movies (
        mid		int,
        title		text,
        year		int,
        runtime	int,
        primary key (mid)
    );'''

    casts = '''
    create table casts (
        mid		int,
        pid		char(4),
        role		text,
        primary key (mid,pid),
        foreign key (mid) references movies,
        foreign key (pid) references moviePeople
    );'''

    recommendations = '''
    create table recommendations (
        watched	int,
        recommended	int,
        score		float,
        primary key (watched,recommended),
        foreign key (watched) references movies,
        foreign key (recommended) references movies
        );'''
    
    customers = '''
    create table customers (
        cid		char(4),
        name		text,
        pwd		text,
        primary key (cid)
    );'''

    sessions = '''
    create table sessions (
        sid		int,
        cid		char(4),
        sdate		date,
        duration	int,
        primary key (sid,cid),
        foreign key (cid) references customers
	        on delete cascade
    );'''

    watch = '''
    create table watch (
        sid		int,
        cid		char(4),
        mid		int,
        duration	int,
        primary key (sid,cid,mid),
        foreign key (sid,cid) references sessions,
        foreign key (mid) references movies
    );'''

    follows = '''
    create table follows (
        cid		char(4),
        pid		char(4),
        primary key (cid,pid),
        foreign key (cid) references customers,
        foreign key (pid) references moviePeople
    );'''

    editors = '''
    create table editors (
        eid		char(4),
        pwd		text,
        primary key (eid)
    );
    '''
    c.execute(moviePeople)
    c.execute(movies)
    c.execute(casts)
    c.execute(recommendations)
    c.execute(customers)
    c.execute(sessions)
    c.execute(watch)
    c.execute(follows)
    c.execute(editors)

    conn.commit()
    return


def main():
    connect("./miniproject1.db")
    define_tables()

    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main()