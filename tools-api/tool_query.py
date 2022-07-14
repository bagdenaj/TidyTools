import csv
import os

import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

conn = psycopg2.connect(
    host="ec2-63-34-180-86.eu-west-1.compute.amazonaws.com",
    database="d8dlmbjnjbhh45",
    user="pbjqydxrhoiqhd",
    password=os.getenv("POSTGRES_PASSWORD"),
)

cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS tools""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS tools (id SERIAL PRIMARY KEY, name VARCHAR(255), """
    """manufacture VARCHAR(255), schedule VARCHAR(255));"""
)


with open("tools.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    for row in tqdm(csv_reader):
        cur.execute(
            """INSERT INTO tools (name, manufacture, schedule) VALUES (%s, %s, %s)""",
            (row["Werkzeug"], row["Hersteller"], "Monthly"),
        )
conn.commit()  # Commit the changes to the database
cur.close()
conn
