import secrets

hash = secrets.token_hex(nbytes=32)
key_exists = False

with open("./.env", "r+") as file:
    lines = file.readlines()
    for line in lines:
        if "TWOFA_KEY" in line:
            key_exists = True
    if not(key_exists):
        file.write(f"\nTWOFA_KEY={hash}")