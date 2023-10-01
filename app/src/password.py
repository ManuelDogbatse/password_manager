import string
import random

# Define all valid characters for passwords
lower = string.ascii_lowercase
upper = string.ascii_uppercase
digit = string.digits
special = string.punctuation
chars = lower + upper + digit + special

def generate_password(pwd_len):
    # Generate random number
    rng = random.SystemRandom()
    # Define password length
    password = ""

    is_valid = False

    while not(is_valid):
        gen_str = ""
        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False

        while len(gen_str) < pwd_len:
            n = rng.randint(0, len(chars) - 1)
            gen_str += chars[n]
        
        # Ensure the password contains at least one character of all types
        for char in gen_str:
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

        if has_lower and has_upper and has_digit and has_special:
            is_valid = True
            password = gen_str

        # print(f"is_valid: {is_valid}")
    return password