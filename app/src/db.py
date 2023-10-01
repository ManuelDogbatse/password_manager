import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()
try:
    connect = psycopg2.connect(host=os.environ.get("POSTGRES_HOST"),
                            database=os.environ.get("POSTGRES_DB"),
                            user=os.environ.get("POSTGRES_USER"),
                            password=os.environ.get("POSTGRES_PASSWORD"),
                            port=os.environ.get("POSTGRES_PORT")
                            )
    print("Connection Successful")
except Exception as e:
    print("Connection Unsuccessful")
    print(e)
    sys.exit(1)