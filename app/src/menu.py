import sys
from time import sleep
from cls import cls
from password import generate_password
from db import connect

NEW_PASSWORD = "1"
SHOW_ONE = "2"
SHOW_ALL = "3"
DELETE_ONE = "4"
UPDATE_2FA = "5"
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
    elif i == UPDATE_2FA:
        return "Update 2FA Authentication"
    elif i == EXIT:
        return "Exit"

def menu():
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("My Password Manager")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Please enter the number for one of the following options:")
    print(f"{NEW_PASSWORD}. {print_menu_option(NEW_PASSWORD)}")
    print(f"{SHOW_ONE}. {print_menu_option(SHOW_ONE)}")
    print(f"{SHOW_ALL}. {print_menu_option(SHOW_ALL)}")
    print(f"{DELETE_ONE}. {print_menu_option(DELETE_ONE)}")
    print(f"{UPDATE_2FA}. {print_menu_option(UPDATE_2FA)}")
    print(f"{EXIT}. {print_menu_option(EXIT)}")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")

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
    elif user_input == UPDATE_2FA:
        cls()
        update_2fa()
        cls()
    elif user_input == EXIT:
        print("Exiting program")
        cls()
        return True
    else:
        print("Invalid Input. Please Try Again")
        sleep(1)
        cls()
    return False
        

def new_password():
    print(f"{print_menu_option(NEW_PASSWORD)}\n")
    website = input("Please enter the name of the website you would like to create a password for:\n")
    email = input("Please enter the email address you will use for the website:\n")
    pwd_len = None
    while not(pwd_len):
        user_input = input("Please enter your desired length of your password. It must be at least 12 characters and at most 255 characters\nEnter:\n")
        if not(user_input.isnumeric()):
            print("Invalid Input. Please Try Again\n")
        elif int(user_input) < 12:
            print("Password Length Too Small. Please Try Again\n")
        elif int(user_input) > 255:
            print("Password Length Too Large. Please Try Again\n")
        else:
            pwd_len = int(user_input)
    print("\nGenerating Password...")
    password = generate_password(pwd_len)
    print("New Password Generated! Here are the details:")
    print(f"\nWebsite: {website}\nEmail Address: {email}\nPassword: {password}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO password(website, email, password) VALUES
                (%s, %s, %s)
            """, [website, email, password])
    input("Press Enter to return to the main menu...\n")

def show_one():
    print(f"{print_menu_option(SHOW_ONE)}\n")
    search = input("Please enter the name of the website that you require the password from:\n")

    with connect:
        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM password WHERE LOWER(website) LIKE %s || '%%'", [search.lower()])
            search_query = cursor.fetchall()

    if len(search_query) == 0:
        print(f"\nPassword for website {search} not found. Would you like to make a password for this website?")
        res = input("Enter y to accept:\n")
        if res.lower() == "y" or res.lower() == "yes":
            cls()
            new_password()
        return
    elif len(search_query) > 1:
        print("\nThere are multiple stored records which match your input. Please select the website and email you require the password from:\n")
        print("Value\tWebsite\tEmail".expandtabs(45))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(len(search_query)):
            print(f"{i+1}.\t{search_query[i][1]}\t{search_query[i][2]}".expandtabs(45))
        print("")
        index = None
        while not(index):
            user_input = input()
            if not(user_input.isnumeric()):
                print("Invalid Input Format. Please Try Again\n")
            elif int(user_input) < 1 or int(user_input) > len(search_query):
                print("Input Out Of Range. Please Try Again\n")
            else:
                index = int(user_input)

        final = search_query[index - 1]
    else:
        final = search_query[0]

    print("\nHere is your password:\n")
    print(f"Website: {final[1]}\nEmail: {final[2]}\nPassword: {final[3]}\n")
    input("Press Enter to return to the main menu...\n")

def show_all():
    print(f"{print_menu_option(SHOW_ALL)}\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM password")
            select_query = cursor.fetchall()

    print("Website\tEmail\tPassword".expandtabs(45))
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in select_query:
        print(f"{row[1]}\t{row[2]}\t{row[3]}".expandtabs(45))
    print("")
    input("Press Enter to return to the main menu...\n")

def delete_one():
    print(f"{print_menu_option(DELETE_ONE)}\n")
    while True:
        print("Delete Login Credentials\n")
        search = input("Please enter the name of the website of the login credentials you would like to delete:\n")

        with connect:
            with connect.cursor() as cursor:
                cursor.execute(f"SELECT * FROM password WHERE LOWER(website) LIKE %s || '%%'", [search.lower()])
                search_query = cursor.fetchall()

    
        if len(search_query) == 0:
            print(f"\nWebsite {search} not found. Would you like to try again?")
            res = input("Enter y/yes to accept:\n")
            if res.lower() == "y" or res.lower() == "yes":
                cls()
                continue
            return
        break

    if len(search_query) > 1:
        print("\nThere are multiple stored records which match your input. Please select the login credentials you would like to delete:\n")
        print("Value\tWebsite\tEmail".expandtabs(45))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(len(search_query)):
            print(f"{i+1}.\t{search_query[i][1]}\t{search_query[i][2]}".expandtabs(45))
        print("")
        index = None
        while not(index):
            user_input = input()
            if not(user_input.isnumeric()):
                print("Invalid Input Format. Please Try Again\n")
            elif int(user_input) < 1 or int(user_input) > len(search_query):
                print("Input Out Of Range. Please Try Again\n")
            else:
                index = int(user_input)

        final = search_query[index - 1]
    else:
        final = search_query[0]

    print("\nAre you sure you would like to delete these user credentials?:\n")
    print(f"Website: {final[1]}\nEmail: {final[2]}\n")
    res = input("Enter y/yes to confirm:\n")
    if res.lower() == "y" or res.lower() == "yes":
        with connect:
            with connect.cursor() as cursor:
                cursor.execute(f"DELETE FROM password WHERE id = %s", [final[0]])
        print("\nCredentials successfully deleted\n")
    else:
        print("\nCredentials not deleted\n")
    input("Press Enter to return to the main menu...\n")

def update_2fa():
    print(f"{print_menu_option(UPDATE_2FA)}\n")