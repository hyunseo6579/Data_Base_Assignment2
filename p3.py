import sqlite3
from random import randint
from datetime import datetime
import math


def p3(cursor, connection, saleinfo, endtime, email):

    print("More information about the sale:")
    cursor.execute('''SELECT s.lister, COUNT(r.reviewer), AVG(r.rating), s.cond
                    FROM sales s LEFT OUTER JOIN bids ON s.sid = bids.sid
                    LEFT OUTER JOIN reviews r ON s.lister = r.reviewee 
                    WHERE s.sid = :sid ;''', {'sid': saleinfo[0]})
    about = cursor.fetchone()
    # saleinfo = [sid, description, max bid/ reserved price, julianday until sale end]
    # endtime = proper time until sale ends
    # about = [lister, count of review on lister, avg rating of lister, sale item condition]
    # sid, lister, #of reviews, avg rating, descr, endtime, cond, maxbid

    print("(SID, lister, No. of lister's reviews, avg rating of the lister, sale descr., time until sale ends, item condition, and max bid/ reserved price)")
    print("%s | %s | %s | %s | %s | %s | %s | %d |" % (saleinfo[0], about[0], str(about[1]), str(about[2]), saleinfo[1], endtime, about[3], saleinfo[2]))

    cursor.execute('''SELECT s.pid FROM sales s 
                    LEFT OUTER JOIN products p ON s.pid = p.pid
                    WHERE s.sid = :sid ;''', {'sid':saleinfo[0]})
    pid = cursor.fetchone()[0]
    if pid is not None:
        print('Information about the product associated to the sale:')
        print("(product description, average rating)")
        cursor.execute('''SELECT descr, IFNULL(AVG(pr.rating),:text) FROM products p 
                        LEFT OUTER JOIN previews pr ON p.pid = pr.pid
                        WHERE p.pid = :pid ;''',
                       {'pid':pid, 'text':'the product is not reviewed'})
        prod_info = cursor.fetchone()
        print('%s | %s\n' % (prod_info[0],str(prod_info[1])))

    print('1. Place bid\n2. List all active sales of this seller\n3. List all reviews of the seller')

    inpt = input("Enter the number of the task you want to perform: ")
    if inpt == '1':
        place_bid(cursor, connection, saleinfo[0], email, saleinfo[2])
    elif inpt == '2':
        list_sales(cursor, about[0], connection, email)
    elif inpt == '3':
        list_rvs(cursor, about[0])
    else:
        print('Entered value is invalid.')
        return

    return


def place_bid(cursor, connect, sid, email, maxbid):

    print("Current highest bid/ reserved price is: %d. You must bid higher than this." % maxbid)
    check = False
    while check == False:
        bid_amt = input("Enter the amount you would like to bid on this sale: ")
        if bid_amt.isdigit() == True:
            if int(bid_amt) > maxbid:
                check = True
            else:
                print("Your bidding must be higher.")
        else:
            print("Entered value is invalid.")

    cursor.execute('SELECT bid FROM bids;')
    bIDs = cursor.fetchall()[0]
    check = False
    while check == False:
        bID = randint(1, 9999)
        x = 'NIL'
        for each_bID in bIDs:
            if str(bID) == each_bID:
                x = each_bID
                break

        if x != 'NIL':
            continue
        else:
            check = True

    bdate = datetime.now()

    cursor.execute('INSERT INTO bids VALUES(:bid, :bidder, :sid, :bdate, :amount) ;',
                   {'bid':bID, 'bidder':email, 'sid':sid, 'bdate':bdate, 'amount':bid_amt})
    connect.commit()

    return


def list_sales(cursor, seller, connection, email):

    cursor.execute('''SELECT s.sid, s.descr, IFNULL(MAX(bids.amount), s.rprice), (julianday(s.edate)- julianday('now'))
                    FROM sales s LEFT OUTER JOIN bids ON s.sid = bids.sid
                    WHERE s.lister = :lister 
                    AND s.edate > date('now')
                    ORDER BY edate ASC ;''', {'lister':seller})

    # from here down is the same as p1.c
    sales = cursor.fetchall()
    print("Active Sales For This Seller:")
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
    p3(cursor, connection, sales[index], time[index], email)

    return


def list_rvs(cursor, seller):

    cursor.execute('''SELECT * FROM reviews WHERE reviewee = :reviewee ; ''', {'reviewee':seller})
    reviews = cursor.fetchall()
    print("%-20s|%-20s|%s|%-20s|%s" % ('Reviewer', 'Reviewee', 'Rating', 'Review Text', 'Date Posted'))
    for each_review in reviews:
        print("%-20s|%-20s|%-6.1f|%-20s|%s" % (each_review[0],each_review[1],each_review[2],each_review[3],each_review[4]))

    return