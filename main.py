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

@app.get('/ingredients')
def get_ingredients():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "select * from ingredients"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    
    ingredients = []
    for row in rows:
        ingredients.append({
            "id": row[0],
            "name": row[1],
            "unit": row[2],
            "price_per_unit": row[3],
            "created_at": row[4],
        })

    return ingredients
    

@app.get('/')
def read_root():
    return {'Message': 'Hello World'}

@app.get('/msg')
def read_msg():
    return {"Message": "Hello"}

@app.get('/items/{id}')
def read_items(id: int):
    return {"item": id}