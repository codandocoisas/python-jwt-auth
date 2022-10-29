import os
import uvicorn
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
from api import app
from database.db import db


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.add_middleware(DBSessionMiddleware,
                   db_url=os.environ["DATABASE_URL"])


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", 
                port=8000, 
                ssl_keyfile=os.path.join(BASE_DIR, "key.pem"), 
                ssl_certfile=os.path.join(BASE_DIR, "cert.pem"))
