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

@app.get('/users')
def read_users():
    cnx = get_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    cnx.close()
    return {"users": users}

@app.get('/')
def read_root():
    return {'Message': 'Hello World'}

@app.get('/msg')
def read_msg():
    return {"Message": "Hello"}

@app.get('/items/{id}')
def read_items(id: int):
    return {"item": id}