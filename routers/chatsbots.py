from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Ensure the Groq API key is set
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("API key for Groq is missing. Please set the GROQ_API_KEY in the .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Define the router
app = APIRouter()

# Pydantic model for user input
class UserInput(BaseModel):
    message: str
    role: str = "user"
    conversation_id: str

# Conversation class to manage chat sessions
class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a compassionate, supportive, and knowledgeable mental health assistant. Your goal is to provide empathetic and non-judgmental support, encourage users to express their feelings, and offer general mental health advice. You do not diagnose or provide medical treatment but can suggest professional help when necessary. Keep responses kind, understanding, and supportive."}
        ]
        self.active: bool = True

# In-memory storage for conversations
conversations: Dict[str, Conversation] = {}

# Helper function to query Groq API
def query_groq_api(conversation: Conversation) -> str:
    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=conversation.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")

# Helper function to get or create a conversation
def get_or_create_conversation(conversation_id: str) -> Conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]

# Chat endpoint
@app.post("/chat/")
async def chat(input: UserInput):
    conversation = get_or_create_conversation(input.conversation_id)

    if not conversation.active:
        raise HTTPException(
            status_code=400, 
            detail="The chat session has ended. Please start a new session."
        )
        
    try:
        # Append the user's message to the conversation
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })
        
        # Query Groq API
        response = query_groq_api(conversation)
        
        # Append the assistant's response to the conversation
        conversation.messages.append({
            "role": "assistant",
            "content": response
        })
        
        return {
            "response": response,
            "conversation_id": input.conversation_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))