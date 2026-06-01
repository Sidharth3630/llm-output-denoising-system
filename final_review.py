# agents/final_review.py
"""
Final Review Agent
Performs comprehensive review and generates the final polished response.
"""

from crewai import Agent, Task


def create_final_reviewer_agent() -> Agent:
    """
    Create and configure the Final Review Agent.
    
    This agent specializes in:
    - Comprehensive quality assurance
    - Ensuring all improvements are cohesive
    - Verifying accuracy, consistency, and conciseness
    - Generating the final polished version
    
    Returns:
        Agent: Configured final review agent
    """
    return Agent(
        role="Final Review and Quality Assurance Expert",
        goal=(
            "Perform a comprehensive final review and generate the best possible version "
            "of the response, ensuring it meets the highest quality standards"
        ),
        backstory=(
            "You are a senior editor and quality assurance specialist with decades of experience. "
            "You have reviewed thousands of documents and know what makes a response excellent. "
            "You understand that the final version must be accurate, consistent, concise, well-written, "
            "and engaging. You have the ability to see the big picture and ensure all components work together harmoniously. "
            "You can refine a response one final time to make it truly outstanding. "
            "Your stamp of approval means the response is ready for any audience."
        ),
        allow_delegation=False,
        verbose=True,
        tools=[]
    )


def create_final_review_task(response_text: str, agent: Agent) -> Task:
    """
    Create a final review task.
    
    Args:
        response_text (str): The final text to review
        agent (Agent): The final review agent
        
    Returns:
        Task: Configured final review task
    """
    return Task(
        description=(
            f"Perform a comprehensive final review of the following response. "
            f"Verify that it is factually accurate, logically consistent, appropriately concise, "
            f"grammatically correct, and professionally written. "
            f"Check that all components work together seamlessly and that the response flows naturally. "
            f"Generate the best possible final version that is ready for the user. "
            f"Ensure it represents the highest quality.\n\n"
            f"Response for final review:\n{response_text}"
        ),
        agent=agent,
        expected_output=(
            "The final, polished version of the response that is ready for the user, "
            "along with a brief summary of the overall quality improvements made throughout the process."
        )
    )
