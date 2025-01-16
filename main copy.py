from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

def get_db_connection():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        database="mydb"
    )
    return  cnx

app = FastAPI()

class ingredient(BaseModel):
    name : str
    unit : str
    price_per_unit : float
    created_at : str

@app.post('/ingredients')
def get_ingredients(ingredient: ingredient):
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