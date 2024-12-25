from fastapi import APIRouter
from .model import handle_user_query

rag_router = APIRouter()

@rag_router.post("/generate-response/")
async def generate_response(user_prompt: str):
    # Process the user's prompt and get the RAG model's response
    response = handle_user_query(user_prompt)
    return {"response": response}
