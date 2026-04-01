from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import logging

from openai_client import OpenAIClient
from notion_client import NotionClient

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AWS Question Answerer", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
openai_client = OpenAIClient()
notion = NotionClient()

# Request/Response models
class MessageHistory(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class QuestionRequest(BaseModel):
    question: str
    conversation_history: list = None  # Optional previous messages for context

class AnswerResponse(BaseModel):
    question: str
    answer: str
    added_to_notion: bool
    message: str
    notion_block_id: Optional[str] = None

class RemoveNotionRequest(BaseModel):
    block_id: str

class RemoveNotionResponse(BaseModel):
    removed: bool
    message: str

# Routes
@app.get("/health")
def health_check():
    """Check if backend and services are healthy"""
    openai_health = openai_client.check_health()
    notion_health = notion.check_connection()

    return {
        "status": "ok" if (openai_health and notion_health) else "degraded",
        "openai": "connected" if openai_health else "disconnected",
        "notion": "connected" if notion_health else "disconnected"
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint: Ask any question, get answer from OpenAI, add to Notion
    """
    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        logger.info(f"Received question: {question}")

        # Build conversation history if provided
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.get("role", "user"), "content": msg.get("content", "")}
                for msg in request.conversation_history
            ]

        # Get answer from OpenAI
        answer = openai_client.generate_response(question, conversation_history=history)

        if answer.startswith("Error:"):
            raise HTTPException(status_code=500, detail=answer)

        logger.info(f"Got answer from OpenAI: {answer[:100]}...")

        # Save to Notion
        notion_added, notion_block_id = notion.add_qa_block(question, answer)

        if notion_added:
            logger.info("Added Q&A to Notion")
            message = "Done ✓ Added to Notion"
        else:
            logger.warning("Failed to add to Notion but got answer")
            message = "Answer received but failed to add to Notion"

        return AnswerResponse(
            question=question,
            answer=answer,
            added_to_notion=notion_added,
            message=message,
            notion_block_id=notion_block_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/remove-notion", response_model=RemoveNotionResponse)
async def remove_notion_block(request: RemoveNotionRequest):
    if not request.block_id:
        raise HTTPException(status_code=400, detail="block_id is required")

    removed = notion.remove_block(request.block_id)
    if removed:
        return RemoveNotionResponse(removed=True, message="Removed from Notion")
    else:
        raise HTTPException(status_code=500, detail="Failed to remove block from Notion")

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "AWS Question Answerer API - Use POST /ask"}

@app.get("/frontend")
def frontend_info():
    return {"info": "Open index.html in your browser"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVER_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)