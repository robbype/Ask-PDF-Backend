from fastapi import FastAPI
from app.api import document
from app.api import message
from app.api import auth
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PDF RAG FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(document.router)
app.include_router(message.router)
app.include_router(auth.router)
