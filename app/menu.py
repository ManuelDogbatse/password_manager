import sys

from password import generate_password
from db import connect

def menu():
    print("------------------------------------------------------------")
    print("Please enter the number for one of the following options:")
    print("1. Generate New Password")
    print("2. Show Specific Password")
    print("3. Show All Passwords")
    print("4. Exit")
    print("------------------------------------------------------------")

    user_input = input()

    if user_input == "1":
        create_row()
    elif user_input == "2":
        print("Show Specific Password")
    elif user_input == "3":
        show_all()
    elif user_input == "4":
        print("Exit")
        sys.exit(0)
    else:
        print("Invalid Input Format. Please Try Again")

def create_row():
    print("\nGenerate New Password\n")
    website = input("Please enter the name of the website you would like to create a password for:\n")
    email = input("Please enter the email address you will use for the website:\n")
    pwd_len = None
    while not(pwd_len):
        user_input = input("Please enter your desired length of your password. It must be at least 12 characters and at most 255 characters\nEnter:\n")
        if not(user_input.isnumeric()):
            print("Invalid Input Format. Please Try Again\n")
        elif int(user_input) < 12:
            print("Password Length Too Small. Please Try Again\n")
        elif int(user_input) > 255:
            print("Password Length Too Large. Please Try Again\n")
        else:
            pwd_len = int(user_input)
    print(f"\npwd_len: {pwd_len}")
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

def show_all():
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM password")
            select_query = cursor.fetchall()
            print("\nWebsite\tEmail\tPassword".expandtabs(20))
            print("------------------------------------------------------------")
            for row in select_query:
                print(f"{row[1]}\t{row[2]}\t{row[3]}".expandtabs(20))
            print("")