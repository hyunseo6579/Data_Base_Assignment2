# This file will contain the functions in order to do the second functionality of the mini project.
# i.e Will be able to search for sales and then retrieve all the active sales.

import math
from p3 import *

def searchForSales(c, conn, user_email):
    print("Please enter all the keywords you wish to search for. (One at a time) Press q to stop entering.")
    keyword_array = []
    # this is so the user can input however many keywords they wish.
    while True:
        user_input = input()
        if user_input == 'q':
            break
        keyword_array.append(user_input)
    result_dictionary = {}
    # query each keyword, then place results into a dictionary to keep count
    for i in range(len(keyword_array)):
        new_keyword = "%" + keyword_array[i] + "%"
        c.execute('''SELECT s1.sid, s1.descr, IFNULL(MAX(b1.amount), s1.rprice)
                FROM sales s1 LEFT OUTER JOIN bids b1 on s1.sid = b1.sid LEFT OUTER JOIN products p1 on s1.pid = p1.pid 
                WHERE JulianDay("now") < JulianDay(s1.edate) AND (s1.descr LIKE :keyword OR p1.descr LIKE :keyword)
                GROUP BY s1.sid, s1.descr;''',
                  {"keyword":new_keyword})
        rows = c.fetchall()
        for i in range(len(rows)):
            if rows[i] in result_dictionary:
                result_dictionary[rows[i]] += 1
            else:
                result_dictionary[rows[i]] = 1
    # this sorts the dictionary
    result_dictionary = sorted(result_dictionary.items(), key=lambda x: x[1], reverse=True)
    # this part is to format the times correctly
    time = []
    for i in range(len(result_dictionary)):
        saleid = result_dictionary[i][0][0]
        c.execute('''SELECT julianday(s1.edate)- julianday("now") 
        FROM sales s1 WHERE s1.sid = :saleid ;''', {"saleid":saleid})
        result_date = c.fetchone()
        day = math.floor(result_date[0])
        hour = math.floor((result_date[0] - day) * 24)
        minute = round(((result_date[0] - day) * 24 - hour) * 60)
        time.append(str(day) + ' day(s) ' + str(hour) + ' hour(s) ' + str(minute) + ' minute(s)')
    # i will list each sale and then prompt the user to choose
    print("These will be the active sales, please use the number in front of the sale to select it.")
    print("The format will be SID, sale description, max bid OR reserved price, and time left until the sale ends.")
    for i in range(len(result_dictionary)):
        print('%d) %s, %s, %s, %s' % (i, result_dictionary[i][0][0], result_dictionary[i][0][1], result_dictionary[i][0][2], time[i]))
    user_choice = int(input("Please select one of the users by using the number in front of their information: "))
    p3(c, conn, result_dictionary[user_choice][0], time[user_choice], user_email)
    return None
