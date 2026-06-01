# agents/consistency_agent.py
"""
Consistency Validation Agent
Checks for contradictions, timeline issues, and logical inconsistencies.
"""

from crewai import Agent, Task


def create_consistency_agent() -> Agent:
    """
    Create and configure the Consistency Validation Agent.
    
    This agent specializes in:
    - Identifying contradictions within the response
    - Detecting timeline inconsistencies
    - Finding logical fallacies and inconsistencies
    - Ensuring statements don't contradict each other
    
    Returns:
        Agent: Configured consistency-checking agent
    """
    return Agent(
        role="Consistency Validation Specialist",
        goal=(
            "Identify and fix contradictions, timeline issues, and logical inconsistencies "
            "to ensure the response flows logically and coherently"
        ),
        backstory=(
            "You are a logical reasoning expert with a talent for spotting inconsistencies and contradictions. "
            "You excel at identifying timeline issues, contradictory statements, logical fallacies, and unclear connections. "
            "Your expertise includes understanding cause-and-effect relationships, temporal sequences, and logical flow. "
            "You ensure that every statement is consistent with others and that the overall narrative is coherent. "
            "You refactor responses to eliminate confusion while maintaining the original intent."
        ),
        allow_delegation=False,
        verbose=True,
        tools=[]
    )


def create_consistency_task(response_text: str, agent: Agent) -> Task:
    """
    Create a consistency validation task.
    
    Args:
        response_text (str): The text to validate
        agent (Agent): The consistency-checking agent
        
    Returns:
        Task: Configured consistency-checking task
    """
    return Task(
        description=(
            f"Carefully review the following response for contradictions and logical inconsistencies. "
            f"Check for timeline issues, statements that contradict each other, and logical fallacies. "
            f"Ensure all claims are consistent with each other and that the logic flows naturally. "
            f"Provide a revised version where logical flow is improved.\n\n"
            f"Response to check:\n{response_text}"
        ),
        agent=agent,
        expected_output=(
            "A detailed analysis of any inconsistencies found, followed by a revised version "
            "of the response with improved logical flow and coherence. "
            "Explain any structural changes made to improve consistency."
        )
    )
