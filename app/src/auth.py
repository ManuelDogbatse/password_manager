import os
import getpass
import pyotp
import base64
import qrcode
from time import sleep
from cls import cls
from dotenv import load_dotenv
from db import connect

def auth_m_pw():
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_config")
            m_pw = cursor.fetchall()[0][0]
    
    print("Welcome to My Password Manager!\n")
    if m_pw:
        m_pw_attempt = getpass.getpass("Please enter your master password:\n")
        with connect:
            with connect.cursor() as cursor:
                cursor.execute("SELECT * FROM auth_config WHERE master_password = %s", [m_pw_attempt])
                is_valid = cursor.fetchall()
        if len(is_valid) == 1:
            return True
        else:
            print("Incorrect Password")
            input("Press Enter to quit...\n")
            return False
    else:
        print("Since this is your first time running this program, you must create a master password to secure your saved passwords")
        print("IMPORTANT NOTICE - Your master password cannot be changed, if you forget it, you will lose access to your saved passwords")
        new_m_pw = getpass.getpass("Please enter your new master password:\n")
        with connect:
            with connect.cursor() as cursor:
                cursor.execute("UPDATE auth_config SET master_password = %s", [new_m_pw])
        print(f"\nMaster password set as {new_m_pw}")
        sleep(3)
        return True
            

def auth_2fa():
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_config")
            is_2fa = cursor.fetchall()[0][1]
    if is_2fa:
        return True
    else:
        print("To further protect your password manager, 2FA is highly recommended.\nWould you like to use 2FA?")
        res = input("Enter y/yes to accept:\n")
        if res.lower() == "y" or res.lower() == "yes":
            key = base64.b32encode(str.encode(os.environ.get("TWOFA_KEY")))
            totp = pyotp.TOTP(key)
            # print(totp.now())
            uri = totp.provisioning_uri(name="user", issuer_name="Password Manager")
            print("Please scan the QR code to add this app to your authenticator app\n")
            print(f"Link: {uri}\n")
            valid_input = False
            while not(valid_input):
                twofa_input = input("Type the 6 digit code on your authenticator app:\n")
                if twofa_input.isdigit():
                    if twofa_input == totp.now():
                        print("\n2FA authentication successfully enabled!\nTo change authenticator app or disable 2FA authentication in the future, select the 'Update 2FA Authentication' option in the main menu")
                        sleep(5)
                        return True
                    else:
                        print("Incorrect code. Please Try Again")
                        # return False
                else:
                    print("Invalid Input. Please Try Again")             
        print("\n2FA authentication disabled.\nTo enable 2FA authentication in the future, select the 'Update 2FA Authentication' option in the main menu")
        sleep(5)
        return True

def auth():
    is_pw_auth = auth_m_pw()
    cls()
    is_2fa_auth = auth_2fa()
    cls()
    return is_pw_auth and is_2fa_auth