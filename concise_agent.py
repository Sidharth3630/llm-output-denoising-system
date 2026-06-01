# agents/concise_agent.py
"""
Conciseness Agent
Removes redundancy, filler words, and unnecessary explanations.
"""

from crewai import Agent, Task


def create_concise_agent() -> Agent:
    """
    Create and configure the Conciseness Agent.
    
    This agent specializes in:
    - Identifying redundant statements
    - Removing filler words and unnecessary explanations
    - Condensing wordy sections into concise statements
    - Maintaining meaning while reducing verbosity
    
    Returns:
        Agent: Configured conciseness agent
    """
    return Agent(
        role="Conciseness Expert",
        goal=(
            "Remove repeated statements, filler words, and unnecessary explanations "
            "while preserving all important meaning and details"
        ),
        backstory=(
            "You are a master of brevity and efficient communication. "
            "You have an exceptional ability to identify redundant statements, "
            "eliminate unnecessary filler words, and condense verbose explanations into concise sentences. "
            "You understand that less is more when it comes to clear communication. "
            "You can reduce word count significantly without sacrificing meaning or losing important information. "
            "You excel at making responses more impactful through conciseness."
        ),
        allow_delegation=False,
        verbose=True,
        tools=[]
    )


def create_concise_task(response_text: str, agent: Agent) -> Task:
    """
    Create a conciseness editing task.
    
    Args:
        response_text (str): The text to make more concise
        agent (Agent): The conciseness agent
        
    Returns:
        Task: Configured conciseness task
    """
    return Task(
        description=(
            f"Review the following response and make it as concise as possible. "
            f"Remove all redundant statements, repeated explanations, and filler words. "
            f"Condense verbose sections into clear, concise statements. "
            f"Preserve all important information and meaning, but eliminate unnecessary words. "
            f"Make every word count.\n\n"
            f"Response to condense:\n{response_text}"
        ),
        agent=agent,
        expected_output=(
            "A concise version of the response with redundancies removed and verbose sections condensed. "
            "Include a summary of what was removed and why. "
            "Ensure no important information is lost in the process."
        )
    )
