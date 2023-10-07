import sys
from cls import cls
from menu import menu
from auth import auth

def main():
    cls()
    if not(auth()):
        sys.exit(0)
    while True:
        if menu():
            break

if __name__ == "__main__":
    main()