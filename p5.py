# This file will contain the functions in order to do the fifth functionality of the mini project.
# i.e Will allow user to search for users and then be able to perform following actions.

import datetime

def searchUsers(c):
    user_input = input("Please enter a keyword to search for: ")
    user_input = '%' + user_input + '%'
    c.execute('SELECT * FROM users WHERE email LIKE :keyword OR name LIKE :keyword ;', {"keyword":user_input})
    rows = c.fetchall()
    return rows

def writeReviewOfUser(c, userInfo, email):
    review_rating = float(input("Please enter a rating from 1 to 5, inclusive: "))
    review_text = input("Please enter the review text for the user: ")
    d = datetime.datetime.today()
    month = d.month
    day = d.day
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    review_date = str(d.year) + '-' + str(month) + '-' + str(day)
    reviewer = email
    reviewee = userInfo[0]
    c.execute('INSERT INTO reviews VALUES(:reviewer, :reviewee, :rating, :rtext, :rdate) ;', {"reviewer":reviewer, "reviewee":reviewee, "rating":review_rating, "rtext":review_text, "rdate":review_date})
    return

