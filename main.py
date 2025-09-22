# main.py

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from crew_agent.email_assistant import run_email_fixer

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI app instance
app = FastAPI(
    title="CrewAI Email Assistant API",
    description="An API to improve and professionalize emails using a CrewAI agent."
)


# Pydantic model for request body validation
class EmailRequest(BaseModel):
    email_text: str


# API endpoint for the email assistant
@app.post("/fix_email")
async def fix_email_endpoint(request: EmailRequest):
    """
    Receives an email from a user and uses the CrewAI agent to rewrite it
    in a professional and clear manner.
    """
    # The user's original email is in request.email_text
    original_email = request.email_text

    # Check if the email text is empty
    if not original_email or len(original_email.strip()) == 0:
        return {"error": "Email text cannot be empty."}

    # Run the CrewAI agent logic
    try:
        professional_email = run_email_fixer(original_email)
        return {"status": "success", "rewritten_email": professional_email}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": "error", "message": "An error occurred while processing the email."}


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    A simple health check to ensure the API is running.
    """
    return {"status": "ok"}