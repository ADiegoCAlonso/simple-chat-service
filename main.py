from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the API
app = FastAPI(title="Single Turn Chatbot")

# Define the expected data structure for the input
class UserRequest(BaseModel):
    message: str

# Define the structure for the output
class BotResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "Service is running"}

# The primary chat endpoint
@app.post("/chat", response_model=BotResponse)
def chat_endpoint(user_request: UserRequest):
    # Log the input (optional, good for debugging)
    print(f"Received message: {user_request.message}")
    
    # Return the constant response as requested
    constant_reply = "I am a simple bot. I always say this."
    
    return {"response": constant_reply}

