import os
from getpass import getpass
from time import sleep
from cls import cls
from password import val_pw
from dotenv import load_dotenv
from db import connect

def auth_m_pw():
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_config")
            m_pw = cursor.fetchall()[0][0]
    
    print("Welcome to My Password Manager!\n")
    if m_pw:
        m_pw_attempt = getpass("Please enter your master password:\n")
        with connect:
            with connect.cursor() as cursor:
                cursor.execute(f"SELECT * FROM auth_config WHERE master_password = %s", [m_pw_attempt])
                is_correct = cursor.fetchall()
        if len(is_correct) == 1:
            return True
        else:
            print("Incorrect Password")
            input("Press Enter to quit...\n")
            return False
    else:
        print("Since this is your first time running this program, you must create a master password to secure your saved passwords")
        print("IMPORTANT NOTICE - Your master password cannot be changed, if you forget it, you will lose access to your saved passwords")
        print("Please create a password with at least:")
        print("One upper case letter")
        print("One lower case letter")
        print("One digit")
        print("One special character (!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)\n")
        new_m_pw = None
        while True:
            new_m_pw = getpass("Please enter your new master password:\n")
            if val_pw(new_m_pw):
                break
            print("Your password doesn't fit the valid password criteria. Please try again.")

        with connect:
            with connect.cursor() as cursor:
                cursor.execute(f"UPDATE auth_config SET master_password = %s", [new_m_pw])
        print(f"\nMaster password set as {new_m_pw}")
        sleep(3)
        return True

def auth():
    is_pw_auth = auth_m_pw()
    cls()
    return is_pw_auth