import sqlite3
import datetime
# commit outside of this file
# postSale(cursor,listerEmail) to run


def getDate(): #HELPER edate
    check = False
    # error checks to makes sure user enters the correct input
    while check == False:
        timeNow = datetime.datetime.today()
        month = timeNow.month
        day = timeNow.day
        if month < 10:
            month = '0' + str(month)
        if day < 10:
            day = '0' + str(day)
        currentDate = str(timeNow.year) + '-' + str(month) + '-' + str(day)
        try:
            complete = input('end date-time (YYYY-MM-DD): ')

            assert(complete > currentDate)
            check = True

        except:
            print('the provided datetime is invalid')
            check = False
    return complete

def pidTaken(pid, c): #HELPER pid
    taken = False
    c.row_factory = sqlite3.Row	

    c.execute("SELECT pid FROM products;")	
    row	= c.fetchone()

    rows = c.fetchall()

    for	each in rows:					
        if pid == str(each["pid"]):
            taken = True


    return taken

def existSID(c): #HELPER sid
    mylist = []

    c.row_factory = sqlite3.Row	

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
    pid = input("Enter product ID (or leave blank): ")
    while pid != "" and (len(pid) > 4 or pid[0].lower() not in alphabet or pidTaken(pid.upper(),c) == False):
        print("Invalid input")
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

    values = (sid, lister, pid, edate, descr, condition, rPrice)
    # insert data into table

    c.execute("INSERT INTO sales(sid, lister, pid, edate, descr, cond, rprice) values (?, ?, ?, ?, ?, ?, ?)", values)
    return None
