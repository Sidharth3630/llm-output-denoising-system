# agents/fact_checker.py
"""
Fact Checking Agent
Validates factual accuracy and detects hallucinations in LLM responses.
"""

from crewai import Agent, Task


def create_fact_checker_agent() -> Agent:
    """
    Create and configure the Fact Checking Agent.
    
    This agent specializes in:
    - Identifying factually incorrect information
    - Detecting hallucinations and false claims
    - Verifying statements against known information
    - Correcting misinformation
    
    Returns:
        Agent: Configured fact-checking agent
    """
    return Agent(
        role="Fact Checking Specialist",
        goal=(
            "Identify and correct any factually incorrect information, "
            "hallucinations, or unverifiable claims in the response"
        ),
        backstory=(
            "You are an expert fact-checker with years of experience in verifying information. "
            "You have a deep understanding of common hallucinations in AI-generated content, "
            "and you know how to identify false claims, incorrect statistics, and made-up references. "
            "Your mission is to ensure that every fact in the response is accurate and trustworthy. "
            "You correct misinformation while preserving the original meaning and structure."
        ),
        allow_delegation=False,
        verbose=True,
        tools=[]
    )


def create_fact_check_task(response_text: str, agent: Agent) -> Task:
    """
    Create a fact-checking task.
    
    Args:
        response_text (str): The text to fact-check
        agent (Agent): The fact-checking agent
        
    Returns:
        Task: Configured fact-checking task
    """
    return Task(
        description=(
            f"Carefully review the following response for factual accuracy. "
            f"Identify any claims that are likely to be false, hallucinated, or unverifiable. "
            f"Flag any inconsistencies with well-known facts. "
            f"Provide a corrected version where necessary.\n\n"
            f"Response to fact-check:\n{response_text}"
        ),
        agent=agent,
        expected_output=(
            "A detailed fact-check report followed by the corrected version of the response. "
            "List any corrections made and explain why they were necessary."
        )
    )
