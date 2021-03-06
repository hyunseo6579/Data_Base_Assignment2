
import sqlite3
from datetime import datetime
import random
import math
import p3


def p1(cursor, connect, user_email):

    cursor.execute('''
        SELECT p.pid, p.descr, COUNT(pr.rid), AVG(pr.rating), COUNT(s.sid)
        FROM products p, sales s
        LEFT OUTER JOIN previews pr ON s.pid = pr.pid
        WHERE p.pid = s.pid
        AND s.edate > date('now')
        GROUP BY p.pid, p.descr
        ORDER BY COUNT(s.sid) DESC ;
    ''')
    rows = cursor.fetchall()
    print("%s|%-20s|%s|%s|%s" % ('PID','Description','No. of Reviews','Avg Rating', 'No. Active Sales'))
    print("_"*67)
    for each_row in rows:
        print("%s|%-20s|%-14s|%-10s|%-16s" % (each_row[0],each_row[1],each_row[2],each_row[3],each_row[4]))

    pid = input("Select a product by entering its PID: ")

    check = False
    for each_row in rows:
        if pid.lower() == each_row[0].lower():
            pid = each_row[0]
            check = True
    if check == False:
        print("Entered PID is invalid.")
        return

    print("1. Write a product review\n"
          "2. List all reviews of the product\n"
          "3. List all active sales of product")
    inpt = input("Enter the task number to perform: ")

    if inpt == '1':
        write_review(cursor, pid, connect, user_email)
    elif inpt == '2':
        view_reviews(cursor, pid)
    elif inpt == '3':
        view_sales(cursor, connect, pid, user_email)
    else:
        print("Entered number is invalid.")

    return


def write_review(cursor, pid, connect, email):
    check = False
    while check == False:
        rtext = input("Enter the review (max 20 characters): ")
        if len(rtext) > 20:
            print("Entered review is too long.")
            check = False
        else:
            check = True
    check = False
    while check == False:
        rating = input("Enter the rating (number between 1 and 5 inclusive): ")
        if rating.isdigit() == True:
            if 5 >= int(rating) >= 1:
                check = True
            else:
                print("Number is not in between 1 and 5.")
                check = False
        else:
            print('Input is not a number.')
            check = False
    check = False

    cursor.execute("SELECT rid FROM previews")
    rids = cursor.fetchall()
    check = False
    while check == False:
        rid = random.randint(1,9999)
        x = 'NIL'
        for each_rid in rids:
            if str(rid) == each_rid[0]:
                x = each_rid[0]
                break

        if x != 'NIL':
            continue

    # does this need to include time as well? check data when posted
    rdate = datetime.now()

    cursor.execute('INSERT INTO previews VALUES(:rid, :pid, :reviewer, :rating, :rtext, :rdate) ;',
                   {'rid':rid, 'pid':pid, 'reviewer':email, 'rating':rating, 'rtext':rtext, 'rdate':rdate})
    connect.commit()

    return

def view_reviews(cursor, pid):

    cursor.execute("SELECT * FROM previews WHERE pid = :pid ;", {'pid':pid})
    reviews = cursor.fetchall()
    print('%s' % 'Product Reviews:')
    for each_review in reviews:
        print(each_review)

    return

def view_sales(cursor, connect, pid, email):

    cursor.execute('''SELECT s.sid, s.descr, IFNULL(MAX(bids.amount), s.rprice), (julianday(s.edate)- julianday('now'))
                    FROM sales s LEFT OUTER JOIN bids ON s.sid = bids.sid
                    WHERE s.pid = :pid 
                    AND s.edate > date('now')
                    GROUP BY s.sid, s.descr
                    ORDER BY edate ASC ;''', {'pid':pid})
    sales = cursor.fetchall()
    print("Active Sales For The Product:")
    print("%-4s|%-25s|%-10s|%s" % ('SID', 'Sale Description', 'Max Bid/RP', 'Time Left Until Sale Ends'))
    time = []
    for each_sale in sales:
        day = math.floor(each_sale[3])
        hour = math.floor((each_sale[3]-day)*24)
        minute = round(((each_sale[3]-day)*24-hour)*60)
        time.append(str(day)+' day(s) '+str(hour)+' hour(s) '+str(minute)+' minute(s)')
    index = 0
    for each_sale in sales:
        print("%-4s|%-25s|%-10d|%s" % (each_sale[0], each_sale[1], each_sale[2], time[index]))
        index += 1

    check = False
    index = -1
    while check == False:
        sid = input("Select a product by entering its SID: ")
        for each_sale in sales:
            index += 1
            if sid.lower() == each_sale[0].lower():
                sid = each_sale[0].lower()
                check = True
                break

        if check == False:
            index = -1
            print("Entered SID is invalid.")

    # prompt p3 options here
    p3.p3(cursor, connect, sales[index], time[index], email)
