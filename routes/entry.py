from fastapi import APIRouter

entry_root=APIRouter()

@entry_root.get("/")
def apirunning():
    res={
        "status":"ok",
        "message":"API is running"
    }
    return res
