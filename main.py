import sqlite3
from os import path
import sys
import getpass
from login import *

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
            pass
            #do 1
        elif user_choice == '2':
            pass
            #do 2
        elif user_choice == '3':
            pass
            #do 3
        elif user_choice == '4':
            pass
            #do 4
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
