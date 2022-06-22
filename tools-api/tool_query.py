import os

import psycopg2

conn = psycopg2.connect(
    host="ec2-63-34-180-86.eu-west-1.compute.amazonaws.com",
    database="d8dlmbjnjbhh45",
    user="pbjqydxrhoiqhd",
    password=os.getenv("POSTGRES_PASSWORD"),
)

manufactures = ["Stihl", "Obi", "ABUS", "Bosch", "HYMER"]

tools = ["Kettensäge", "Presslufthammer", "Schleifgerät", "Nagel"]

cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS tools (id SERIAL PRIMARY KEY, name VARCHAR(255), """
    """manufacture VARCHAR(255), schedule VARCHAR(255))"""
)
for tool in tools:
    for manf in manufactures:
        cur.execute(
            """INSERT INTO tools (name, manufacture, schedule) VALUES (%s, %s, %s)""",
            (tool, manf, "Monthly"),
        )
conn.commit()  # Commit the changes to the database
cur.close()
conn.close()
