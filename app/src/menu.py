import sys
from cls import cls
from password import generate_password
from db import connect

def menu():
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("My Password Manager")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Please enter the number for one of the following options:")
    print("1. Generate New Password")
    print("2. Show Specific Password")
    print("3. Show All Passwords")
    print("4. Exit")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")

    user_input = input()

    if user_input == "1":
        cls()
        create_row()
        cls()
    elif user_input == "2":
        cls()
        show_one()
        cls()
    elif user_input == "3":
        cls()
        show_all()
        cls()
    elif user_input == "4":
        print("Exiting program\n")
        cls()
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
    print("\nShow Specific Password\n")
    search = input("Please enter the name of the website that you require the password from:\n")

    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM password WHERE LOWER(website) LIKE %s || '%%'", [search.lower()])
            search_query = cursor.fetchall()

    if len(search_query) == 0:
        print(f"\nPassword for website {search} not found. Would you like to make a password for this website?")
        res = input("Enter y to accept:\n")
        if res.lower() == "y" or res.lower() == "yes":
            cls()
            create_row()
        return

    if len(search_query) > 1:
        print("\nThere are multiple stored records which match your input. Please select the website and email you require the password from:\n")
        print("Value\tWebsite\tEmail".expandtabs(45))
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
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
    print("\nShow All Passwords\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM password")
            select_query = cursor.fetchall()

    print("Website\tEmail\tPassword".expandtabs(45))
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for row in select_query:
        print(f"{row[1]}\t{row[2]}\t{row[3]}".expandtabs(45))
    print("")
    input("Press Enter to return to the main menu...\n")