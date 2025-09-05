from mysql import MySql
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.post("/get/category/list")
def CategoryGetList():
    ms = MySql()
    sql = 'select * from category;'
    result = ms.execute(sql)
    print(result)
    return result

@app.post("/get/content/list")
def ContentGetList():
    ms = MySql()
    sql = 'select * from content;'
    result = ms.execute(sql)
    print(result)
    return result