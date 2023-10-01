from menu import menu

# with connect:
#     with connect.cursor() as cursor:
#         # cursor.execute("""
#         #     CREATE TABLE password(
#         #         id SERIAL PRIMARY KEY,
#         #         website VARCHAR NOT NULL,
#         #         email VARCHAR NOT NULL,
#         #         password VARCHAR NOT NULL UNIQUE
#         #     )
#         # """)

print("------------------------------------------------------------")
print("Welcome To My Password Manager!")
while True:
    menu()