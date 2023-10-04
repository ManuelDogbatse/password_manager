import sys
import getpass
import time
from cls import cls
from menu import menu
from db import connect

cls()
with connect:
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM master_password")
        m_pwd = cursor.fetchall()[0][0]

if not(m_pwd):
    print("Welcome to My Password Manager!\n")
    print("Since this is your first time running this program, you must create a master password to secure your saved passwords")
    new_m_pwd = getpass.getpass("Please enter your new master password:\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("UPDATE master_password SET password = %s", [new_m_pwd])
    print(f"\nMaster password set as {new_m_pwd}")
    time.sleep(3)
    cls()

else:
    print("Welcome to My Password Manager!\n")
    m_pwd_attempt = getpass.getpass("Please enter your master password:\n")
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM master_password WHERE password = %s", [m_pwd_attempt])
            is_valid = cursor.fetchall()
    if len(is_valid) == 1:
        cls()
    else:
        print("Incorrect Password")
        input("Press Enter to quit...\n")
        cls()
        sys.exit(0)

while True:
    menu()