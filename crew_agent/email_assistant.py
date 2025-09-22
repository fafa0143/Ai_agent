# crew_agent/email_assistant.py

import os
from crewai import LLM, Agent, Task, Crew


def get_email_crew():
    """
    Initializes and returns the CrewAI Crew for email assistance.
    """
    llm = LLM(
        model=os.getenv("GEMINI_MODEL", "gemini/gemini-2.0-flash"),
        temperature=float(os.getenv("GEMINI_TEMPERATURE", 0.1))
    )

    email_assistant = Agent(
        role="email assistant agent",
        goal="improve emails and make them sound professional and clear",
        backstory="a highly experienced communication expert skilled in email writing",
        verbose=True,
        llm=llm
    )

    # Note: The task is not defined here because it depends on the user's input.
    # It will be created dynamically in the FastAPI endpoint.

    return email_assistant


def run_email_fixer(original_email: str) -> str:
    """
    Runs the CrewAI process to fix an email and returns the result.
    """
    email_assistant = get_email_crew()

    email_task = Task(
        description=f"""Take the following email and rewrite it in a professional and clear manner for 
        excellent verbal and writing communication. Expand abbreviations:'''{original_email}'''""",
        agent=email_assistant,
        expected_output="a professional written email with a proper format"
    )

    crew = Crew(
        agents=[email_assistant],
        tasks=[email_task],
        verbose=True
    )

    result = crew.kickoff()
    return result