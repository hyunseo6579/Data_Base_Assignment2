import sqlite3
from datetime import datetime, date
# call the imports here

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def drop_tables():
    global connection, cursor

    drops = ["drop table if exists previews;", "drop table if exists reviews;",
             "drop table if exists bids;","drop table if exists sales;",
             "drop table if exists products;", "drop table if exists users;"]

    # maybe try: cursor.executemany("drop table if exists ?", drops) where drops = different tables
    for i in range(6):
        cursor.execute(drops[i])


def define_tables():
    global connection, cursor

    tables = ['''
    create table users (
      email		char(20),
      name		char(16),
      pwd		char(4),
      city		char(15),
      gender	char(1),
      primary key (email)
    );        
    ''',
    '''
    create table products (
      pid		char(4),
      descr		char(20),
      primary key (pid)
    );
    ''',
    '''
    create table sales (
      sid		char(4),
      lister	char(20) not null,
      pid		char(4),
      edate		date,
      descr		char(25),
      cond		char(10),
      rprice	int,
      primary key (sid),
      foreign key (lister) references users,
      foreign key (pid) references products
    );
    ''',
    '''
    create table bids (
      bid		char(20), 
      bidder	char(20) not null,
      sid		char(4) not null, 
      bdate 	date, 
      amount	float,
      primary key (bid),
      foreign key (bidder) references users,
      foreign key (sid) references sales
    );
    ''',
    '''
    create table reviews (
      reviewer	char(20), 
      reviewee	char(20), 
      rating	float, 
      rtext		char(20), 
      rdate		date,
      primary key (reviewer, reviewee),
      foreign key (reviewer) references users,
      foreign key (reviewee) references users
    );
    ''',
    '''
    create table previews (
      rid		int,
      pid		char(4),
      reviewer	char(20) not null,
      rating	float,
      rtext		char(20),
      rdate		date,
      primary key (rid),
      foreign key (pid) references products,
      foreign key (reviewer) references users
    );
    ''']

    for i in range(len(tables)):
        cursor.execute(tables[i])
    connection.commit()

    return


def insert_data():  # this may need to be deleted for demo as db may already have datas
    global connection, cursor

    cursor.executescript(''' insert into users values ('mc@gmail.com','Michael Choi','abcd','Edmonton, AB','M');
        insert into users values ('tedwalsh@td.com','Ted Walsh','7632','Calgary, Ab','M');
        insert into users values ('hm@mah.com','Harry Mah','1453','Waterloo, ON','M');
        insert into users values ('ks@gmail.com','Kaitlyn Scott','pqwe','Toronto, ON','F');
        insert into users values ('angels@gmail.com','Angel Silverman','anlo','Vancouver, BC','F');
        insert into users values ('mk@abc.com','Maximillion Kung','0931','Burnaby, BY','F');
        insert into users values ('davood@gmail.com','Davood Rafiei','1234','Edmonton, AB','M');
        insert into products values ('N01', 'Nikon F100');
        insert into products values ('N02', 'Nikon D3500');
        insert into products values ('B01', 'BMW M8');
        insert into products values ('P01', 'Porsche 911');
        insert into products values ('P02', 'Porsche 918');
        insert into sales values ('S01', 'mc@gmail.com', 'N01', '2016-03-24', 'Camera Sale', 'Brand new', 1400);
        insert into sales values ('S02', 'mc@gmail.com', 'N02', '2018-09-02', 'Great deal', 'Used', 698);
        insert into sales values ('S03', 'hm@mah.com', 'N02', '2015-12-12', 'End year', 'New', 530);
        insert into sales values ('S04', 'ks@gmail.com', 'P01', '2019-01-11', 'Amazing', 'New', 30000000);
        insert into bids values ('B01', 'hm@mah.com', 'S01', '2016-04-01', 1405.02);
        insert into bids values ('B02', 'ks@gmail.com', 'S01', '2016-04-02', 1407.99);
        insert into bids values ('B03', 'hm@mah.com', 'S02', '2018-09-11', 999);
        insert into bids values ('B04', 'angels@gmail.com', 'S03', '2016-01-03', 430);
        insert into bids values ('B05', 'tedwalsh@td.com', 'S04', '2019-05-19', 39099999);
        insert into reviews values ('mc@gmail.com', 'tedwalsh@td.com', 4.9, 'great guy!', '2016-05-02');
        insert into reviews values ('hm@mah.com', 'ks@gmail.com', 5.0, 'car is amazing', '2015-09-02');
        insert into reviews values ('angels@gmail.com', 'mc@gmail.com', 0.5, '', date('now','-4 years'));
        insert into previews values (1, 'N01', 'hm@mah.com', 1.5, 'definitly used', '2016-04-25');
        insert into previews values (2, 'N02','ks@gmail.com', 2, 'great quality', '2018-09-11');
        insert into previews values (3, 'P02', 'mk@abc.com', 5, 'amazing car', date('now','-9 months'));''')

    connection.commit()
    return




def getDate(): #HELPER edate
    check = False
    # error checks to makes sure user enters the correct input
    while check == False:
        timeNow = datetime.now(tz=None)
        try:
            complete = input('end date-time (YYYY-MM-DD-HH-MM): ')
            complete_date = complete.split('-')

            given = datetime(
                int(complete_date[0]),
                int(complete_date[1]), 
                int(complete_date[2]),
                int(complete_date[3]), 
                int(complete_date[4]) )
            assert(given>timeNow)
            check = True

        except:
            print('the provided datetime is invalid')
            check = False
    return given

def pidTaken(pid, c): #HELPER pid
    taken = False

    #conn = sqlite3.connect('./movies.db')
    c.row_factory = sqlite3.Row	
    #c = conn.cursor()

    c.execute("SELECT pid FROM products;")	
    row	= c.fetchone()

    rows = c.fetchall()

    for	each in rows:					
        if pid == str(each["pid"]):
            taken = True


    return taken

def existSID(c): #HELPER sid
    mylist = []

    #conn = sqlite3.connect('./movies.db')
    c.row_factory = sqlite3.Row	
    #c = conn.cursor()

    c.execute("SELECT sid FROM sales;")	
    rows = c.fetchall()
    for	each in rows:					
        mylist.append(str(each["sid"]))
    return mylist

def postSale(c, lister):

    # get PID
    alphabet = ['a','b','c','d','e','f','g','h','i','j',
               'k','l','m','n','o','p','q','r','s','t',
               'u','v','w','x','y','z']
    pid = input("Enter product ID (or leave balnk): ")
    while pid != "" and (len(pid) > 4 or pid[0].lower() not in alphabet or pidTaken(pid.upper(),c) == True):
        print("Invalid input or pid already taken")
        pid = input("Enter product ID (or leave blank): ")
    if pid == "":
        pid = None
        
    # get edate as datetime object
    edate = getDate()

    #gets prodct description
    descr = input("product description: ")
    while descr == "":
        print("Invalid description (cannot be blank)")
        descr = input("product description: ")

    # gets condtion
    conditionTypes = ["mint", "new", "used", "broken"]
    condition = input("condition of product (Mint, New, Used, broken): ")
    while condition.lower() not in conditionTypes:
        print("Please choose a valid condtion")
        condition = input("condition of product (Mint, New, Used, broken): ")
    condition = condition.capitalize()

    # gets reserved price
    rPrice = input("reservered price (or leave blank): ")
    while rPrice != "" and (rPrice.isdigit() == False and rPrice.isdecimal() == False):
        print("Invalid input. must be number or blank")
        rPrice = input("reservered price (or leave blank): ")
    if rPrice == "":
        rPrice = None
    else: rPrice = int(rPrice)

    #find unique sid
    sidExist = existSID(c)
    for i in range(1,100):
        if i<10: 
            sid = "S0"+str(i)
        else:
            sid = "S"+str(i)
        if sid not in sidExist:
            break


    # insert data into table
    #conn = sqlite3.connect('./movies.db')	
    c.executescript("INSERT INTO sales(sid, lister, pid, edate, descr, cond, rprice) values (?, ?, ?, ?, ?)",
     (sid, lister, pid, edate, descr, condition, rPrice))
    #conn.commit()
    #conn.close()
    return None


def main():
    global connection, cursor

    path = './' + input("Enter your database file name: ")
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    

    # insert operations:
    lister = "BillyBob"
    postSale(cursor, lister)
    # insert above ^

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
