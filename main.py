from fastapi import FastAPI
import mysql.connector

def get_db_connection():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        database="mydb"
    )
    return  cnx

app = FastAPI()

@app.get('/')
def read_root():
    return {'Message': 'Hello World'}

@app.get('/msg')
def read_msg():
    return {"Message": "Hello"}

@app.get('/items/{id}')
def read_items(id: int):
    return {"item": id}