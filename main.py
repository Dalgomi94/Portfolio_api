from mysql import MySql
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.post("/get/category/list")
def CategoryGetList():
    ms = MySql()
    
    return {"Hi": "World"}