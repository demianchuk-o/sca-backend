from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base_class import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spy Cat Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
def read_root():
    return {"status": "ok", "message": "Welcome to the Spy Cat Agency API!"}