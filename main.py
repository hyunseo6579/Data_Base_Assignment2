import sqlite3
from os import path
import sys
import getpass
from login import *
from p5 import *
from p2 import *
from p4 import *
from p1 import *

# With db argument passed in, checks if it's a valid file. If valid connect and make cursor, if not print error and exit
db_name = sys.argv[1]
if path.exists(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
else:
    print("Error: Database not found.")
    exit()
#this is the main program loop, which will contain a logged in loop to make sure the user successfully logs in.
program_active = True
while program_active:
    user_email = input("Please enter your email or q to quit: ")
    if user_email == 'q':
        exit()
    if not('@' in user_email):
        print("Please enter a valid email.")
        continue
    user_pass = getpass.getpass(prompt='Please enter your password: ')
    logged_in = login(c, conn, user_email, user_pass)
    if not logged_in:
        print("Error: Unsuccessful login.")
        continue
    while logged_in:
        # have all the options when logged in successfully, then ask user which they wish to do
        print("Enter one of the following numbers in order to complete an action")
        print("1: List products")
        print("2: Search for sales")
        print("3: Post a sale")
        print("4: Search for users")
        print("5: Logout")
        print("6: Exit")
        user_choice = input()
        if user_choice == '1':
            p1(c, conn, user_email)
        elif user_choice == '2':
            searchForSales(c, conn, user_email)
        elif user_choice == '3':
            postSale(c, user_email)
            conn.commit()
        elif user_choice == '4':
            # search up all the users, list them out and then ask what individual the user wishes to select.
            users_list = searchUsers(c)
            count_of_users = len(users_list)
            print("Please use the integer in front of the user to select that individual.")
            for i in range(count_of_users):
                print('%d) %s, %s, %s' % (i, users_list[i][0], users_list[i][1], users_list[i][3]))
            # now select an action and perform the action with the selected user.
            selected_user = int(input("Please enter the integer of the individual you wish to select: "))
            print("Please select a following action")
            print("1: Write a review of the user")
            print("2: List all active listings of the user")
            print("3: List all reviews of the user")
            selected_action = input()
            if selected_action == '1':
                writeReviewOfUser(c, users_list[selected_user], user_email)
            elif selected_action == '2':
                c.execute('''SELECT * FROM sales s1 WHERE s1.lister = :selecteduser;''', {"selecteduser":users_list[selected_user][0]})
                temp_rows = c.fetchall()
                if len(temp_rows) == 0:
                    print("This user does not have any active sales.")
                else:
                    list_sales(c, users_list[selected_user][0], conn, user_email)
            elif selected_action == '3':
                list_rvs(c, users_list[selected_user][0])
            conn.commit()
        elif user_choice == '5':
            # code to logout of current user
            print("Logging out.")
            logged_in = False
        elif user_choice == '6':
            # code to log out & then exit out of the program
            print("Exiting.")
            logged_in = False
            program_active = False
        else:
            # if this is reached, it means the user didn't input a valid response.
            print("Please enter a valid choice.")

# commit for the final time and then close the connection & finish the program
conn.commit()
conn.close()
exit()
