import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()
try:
    connect = psycopg2.connect(host=os.environ.get("PG_HOST"),
                            database=os.environ.get("PG_DATABASE"),
                            user=os.environ.get("PG_USER"),
                            password=os.environ.get("PG_PASSWORD"),
                            port=os.environ.get("PG_PORT")
                            )
    print("Connection Successful")
except Exception as e:
    print("Connection Unsuccessful")
    print(e)
    sys.exit(1)