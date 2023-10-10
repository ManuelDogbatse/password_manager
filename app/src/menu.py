import sys
from getpass import getpass
from time import sleep
from cls import cls
from password import gen_pw
from db import connect

NEW_PASSWORD = "1"
SHOW_ONE = "2"
SHOW_ALL = "3"
DELETE_ONE = "4"
DELETE_ALL = "5"
EXIT = "6"

def print_menu_option(i):
    if i == NEW_PASSWORD:
        return "Generate New Password"
    elif i == SHOW_ONE:
        return "Show Login Credential"
    elif i == SHOW_ALL:
        return "Show All Login Credentials"
    elif i == DELETE_ONE:
        return "Delete Login Credential"
    elif i == DELETE_ALL:
        return "Delete All Login Credentials"
    elif i == EXIT:
        return "Exit"

def menu():
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    print("My Password Manager")
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    print("Please enter the number for one of the following options:")
    print(f"{NEW_PASSWORD}. {print_menu_option(NEW_PASSWORD)}")
    print(f"{SHOW_ONE}. {print_menu_option(SHOW_ONE)}")
    print(f"{SHOW_ALL}. {print_menu_option(SHOW_ALL)}")
    print(f"{DELETE_ONE}. {print_menu_option(DELETE_ONE)}")
    print(f"{DELETE_ALL}. {print_menu_option(DELETE_ALL)}")
    print(f"{EXIT}. {print_menu_option(EXIT)}")
    print("--------------------------------------------------------------------------------------------------------------------------------------------")

    user_input = input()

    if user_input == NEW_PASSWORD:
        cls()
        new_password()
        cls()
    elif user_input == SHOW_ONE:
        cls()
        show_one()
        cls()
    elif user_input == SHOW_ALL:
        cls()
        show_all()
        cls()
    elif user_input == DELETE_ONE:
        cls()
        delete_one()
        cls()
    elif user_input == DELETE_ALL:
        cls()
        delete_all()
        cls()
    elif user_input == EXIT:
        print("Exiting program")
        cls()
        return False
    else:
        print("Invalid Input. Please Try Again")
        sleep(1)
        cls()
    return True
        

def new_password():
    print(f"{print_menu_option(NEW_PASSWORD)}\n")
    website = input("Please enter the name of the website you would like to create login credentials for:\n")
    email = input("Please enter the email address you will use for the website:\n")
    pw_len = None
    while not(pw_len):
        user_input = input("Please enter your desired length of your password. It must be at least 12 characters and at most 255 characters\nEnter:\n")
        if not(user_input.isnumeric()):
            print("Invalid Input. Please Try Again\n")
        elif int(user_input) < 12:
            print("Password Length Too Small. Please Try Again\n")
        elif int(user_input) > 255:
            print("Password Length Too Large. Please Try Again\n")
        else:
            pw_len = int(user_input)
    print("\nGenerating Password...")
    password = gen_pw(pw_len)
    print("New Password Generated! Here are the details:")
    print(f"\nWebsite: {website}\nEmail Address: {email}\nPassword: {password}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO login_cred(website, email, password) VALUES
                (%s, %s, %s)
            """, [website, email, password])
    input("Press Enter to return to the main menu...\n")

def show_one():
    print(f"{print_menu_option(SHOW_ONE)}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM login_cred")
            select_query = cursor.fetchall()

    if len(select_query) == 0:
        print("You have no login credentials to show\n")
        input("Press Enter to return to the main menu...\n")
        return

    print("Please enter the ID of the login credentials you need:\n")
    print("ID\tWebsite\tEmail".expandtabs(45))
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(select_query)):
        print(f"{i+1}.\t{select_query[i][1]}\t{select_query[i][2]}".expandtabs(45))
    print("")
    index = None
    while True:
        user_input = input("Enter ID (or enter 'b' to return to the main menu):\n")
        if not(user_input.isnumeric()):
            if user_input == "b":
                return
            print("Invalid Input Format. Please Try Again\n")
        elif int(user_input) < 1 or int(user_input) > len(select_query):
            print("Input Out Of Range. Please Try Again\n")
        else:
            index = int(user_input) - 1
            break

    print("\nHere is your password:\n")
    print(f"Website: {select_query[index][1]}\nEmail: {select_query[index][2]}\nPassword: {select_query[index][3]}\n")
    input("Press Enter to return to the main menu...\n")

def show_all():
    print(f"{print_menu_option(SHOW_ALL)}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM login_cred")
            select_query = cursor.fetchall()
    
    if len(select_query) == 0:
        print("You have no login credentials to show\n")
        input("Press Enter to return to the main menu...\n")
        return

    print("Website\tEmail\tPassword".expandtabs(45))
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    for row in select_query:
        print(f"{row[1]}\t{row[2]}\t{row[3]}".expandtabs(45))
    print("")
    input("Press Enter to return to the main menu...\n")

def delete_one():
    print(f"{print_menu_option(DELETE_ONE)}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM login_cred")
            select_query = cursor.fetchall()
    
    if len(select_query) == 0:
        print("You have no login credentials to show\n")
        input("Press Enter to return to the main menu...\n")
        return

    print("Please enter the ID of the login credentials you would like to delete:\n")
    print("ID\tWebsite\tEmail".expandtabs(45))
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(select_query)):
        print(f"{i+1}.\t{select_query[i][1]}\t{select_query[i][2]}".expandtabs(45))
    print("")
    index = None
    while True:
        user_input = input("Enter ID (or enter 'b' to return to the main menu):\n")
        if not(user_input.isnumeric()):
            if user_input == "b":
                return
            print("Invalid Input Format. Please Try Again\n")
        elif int(user_input) < 1 or int(user_input) > len(select_query):
            print("Input Out Of Range. Please Try Again\n")
        else:
            index = int(user_input) - 1
            break

    print("\nAre you sure you would like to delete these login credentials?:\n")
    print(f"Website: {select_query[index][1]}\nEmail: {select_query[index][1]}\n")
    res = input("Enter y/yes to confirm:\n")
    if res.lower() == "y" or res.lower() == "yes":
        with connect:
            with connect.cursor() as cursor:
                cursor.execute(f"DELETE FROM login_cred WHERE id = %s", [select_query[index][0]])
        print("\nLogin credentials successfully deleted\n")
    else:
        print("\nCredentials not deleted\n")
    input("Press Enter to return to the main menu...\n")

def delete_all():
    print(f"{print_menu_option(DELETE_ALL)}\n")

    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM login_cred")
            select_query = cursor.fetchall()
    
    if len(select_query) == 0:
        print("You have no login credentials to show\n")
        input("Press Enter to return to the main menu...\n")
        return
    
    print("Are you sure you would like to delete all of your login credentials?:\n")
    res = input("Enter y/yes to confirm:\n")
    if res.lower() == "y" or res.lower() == "yes":
        while True:
            m_pw = getpass("\nPlease re-enter your master password to confirm this decision (or enter 'b' to return to the main menu):\n")
            if m_pw == "b":
                return
            with connect:
                with connect.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM auth_config WHERE master_password = %s", [m_pw])
                    is_correct = cursor.fetchall()
            if len(is_correct) == 1:
                with connect:
                    with connect.cursor() as cursor:
                        cursor.execute(f"TRUNCATE TABLE login_cred")
                        print("All login credentials successfully deleted\n")
                break
            else:
                print("Incorrect master password. Please try again")
    else:
        print("\nCredentials not deleted\n")
    input("Press Enter to return to the main menu...\n")