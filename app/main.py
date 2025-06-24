from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import defer

from app.api.api import api_router
from app.db.session import engine
from app.db.base_class import Base

def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)

def get_app():
    """Create and return the FastAPI application instance."""
    app = FastAPI(title="Spy Cat Agency API")
    app.include_router(api_router)
    return app

app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()
