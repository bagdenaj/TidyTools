import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="ec2-63-34-180-86.eu-west-1.compute.amazonaws.com",
    database="d8dlmbjnjbhh45",
    user="pbjqydxrhoiqhd",
    password=os.getenv("POSTGRES_PASSWORD"),
)

manufactures = ["Stihl", "Obi", "ABUS", "Bosch", "HYMER"]


cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS manufacture (id SERIAL PRIMARY KEY, name VARCHAR(255))"
)

with open("werkzeughersteller.txt", "r", encoding="utf-8") as file:
    manufactures = file.readlines()
    for manufactur in manufactures:
        cur.execute(
            """INSERT INTO manufacture (name) VALUES (%s)""", (manufactur.strip(),)
        )

conn.commit()
cur.close()
conn.close()
