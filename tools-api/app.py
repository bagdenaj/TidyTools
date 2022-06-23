import os

import psycopg2
from fastapi import FastAPI

app = FastAPI()


def get_cursor():
    conn = psycopg2.connect(
        host="ec2-63-34-180-86.eu-west-1.compute.amazonaws.com",
        database="d8dlmbjnjbhh45",
        user="pbjqydxrhoiqhd",
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    return conn.cursor()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_manufactures")
def get_manufactures():
    with get_cursor() as cur:
        cur.execute("SELECT name FROM manufacture")
        manufactures = cur.fetchall()
        cur.close()
        return manufactures


@app.get("/get_tools/{seleceted_manufacturer}")
def get_tools(seleceted_manufacturer: str):
    # query tools according to selected manufacturer
    with get_cursor() as cur:
        cur.execute(
            "SELECT name FROM tools WHERE manufacture=(%s)", (seleceted_manufacturer,)
        )
        tools = cur.fetchall()
        cur.close()
        return tools


@app.get("/get_schedule/{tool}")
def get_schedule(tool: str):
    with get_cursor() as cur:
        cur.execute("SELECT schedule FROM tools WHERE name=(%s)", (tool,))
        schedule = cur.fetchone()
        cur.close()
        return schedule
