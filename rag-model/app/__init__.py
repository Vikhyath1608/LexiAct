from fastapi import FastAPI

app = FastAPI()

# Import the routes from api.py
from .api import rag_router

# Include the RAG API routes
app.include_router(rag_router)
