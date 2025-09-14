import json
from mysql import MySql
from fastapi import FastAPI, Response, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from typing_extensions import Annotated

app = FastAPI()

def get_user_list_dep(active: Optional[int] = None, role: Optional[str] = None):
    return {"active": active, "role": role}

@app.post("/get/user/list")
def UserGetList():
    try:
        ms = MySql(is_local=False)   # ✅ 로컬에서도 127.0.0.1 강제 X, config.json 그대로 사용
        result = ms.execute('select * from user;')
        return result                 # (list[dict])면 그대로 OK
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

class GetContentList(BaseModel):
    target : Optional[int] = None

@app.post("/get/category/list")
def CategoryGetList():
    try:
        ms = MySql(is_local=False)   # ✅ 로컬에서도 127.0.0.1 강제 X, config.json 그대로 사용
        result = ms.execute('select * from category;')
        return result                 # (list[dict])면 그대로 OK
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

class GetContentList(BaseModel):
    target : Optional[int] = None

@app.post("/get/content/list")
def ContentGetList(res : Response, request : Request, data: GetContentList = Depends()):
    ms = MySql(is_local=False)

    if data.target:
        sql = '''
                select
                content.seq,
                category.name as category,
                content.title,
                content.content,
                user.nickname as writer,
                date_format(content.datetime, '%%Y-%%m-%%d %%H:%%i:%%s') as datetime
            from content
            left join category on category.seq = content.category
            left join user on user.seq = content.seq
            where
                content.is_view = 1 and
                content.is_delete = 0 and
                content.is_temp = 0 and
                content.category = %s;
        '''
        values = (data.target,)
        result = ms.execute(sql, values)
    else:
        sql = '''
            select
                seq,
                category,
                title,
                content,
                writer,
                date_format(datetime, '%Y-%m-%d %H:%i:%s') as datetime
            from content
            where
                is_view = 1 and
                is_delete = 0 and
                is_temp = 0;
        '''
        result = ms.execute(sql)
    if result:
        return Response(status_code=status.HTTP_200_OK, content=json.dumps(result), media_type='application/json')
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content Not Found")
