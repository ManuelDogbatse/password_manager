import string
import random

# Define all valid characters for passwords
lower = string.ascii_lowercase
upper = string.ascii_uppercase
digit = string.digits
special = string.punctuation
chars = lower + upper + digit + special

def gen_pw(pw_len):
    # Generate random number
    rng = random.SystemRandom()
    # Define password length
    pw = None

    while True:
        pw = ""

        while len(pw) < pw_len:
            n = rng.randint(0, len(chars) - 1)
            pw += chars[n]
        

        if val_pw(pw):
            break

    return pw

# Validate password
def val_pw(pw):
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    # Ensure the password contains at least one character of all types
    for char in pw:
        if char in lower:
            has_lower = True
            continue
        if char in upper:
            has_upper = True
            continue
        if char in digit:
            has_digit = True
            continue
        if char in special:
            has_special = True

    return has_lower and has_upper and has_digit and has_special