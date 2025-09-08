from mysql import MySql
from fastapi import FastAPI
from fastapi.responses import JSONResponse  # 개발 중 에러 보기용(선택)

app = FastAPI()

@app.post("/get/category/list")
def CategoryGetList():
    try:
        ms = MySql(is_local=False)   # ✅ 로컬에서도 127.0.0.1 강제 X, config.json 그대로 사용
        result = ms.execute('select * from category;')
        return result                 # (list[dict])면 그대로 OK
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

@app.post("/get/content/list")
def ContentGetList():
    try:
        ms = MySql(is_local=False)   # ✅
        result = ms.execute('select * from content;')
        return result
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
