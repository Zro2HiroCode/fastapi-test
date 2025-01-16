from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

# Create a connection pool
dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USERNAME"),
    "database": os.getenv("MYSQL_DATABASE"),
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def get_db_connection():
    return cnxpool.get_connection()

app = FastAPI()

class ingredient(BaseModel):
    name : str
    unit : str
    price_per_unit : float
    created_at : str

@app.post('/ingredients')
def create_ingredient(ingredient: ingredient):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = '''
    insert into ingredients (name, unit, price_per_unit, created_at)
    values (%s, %s, %s, %s)
    '''
    cursor.execute(query, (ingredient.name, ingredient.unit, 
                           ingredient.price_per_unit, ingredient.created_at))
    cnx.commit()
    ingredient_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return {"id": ingredient_id}

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