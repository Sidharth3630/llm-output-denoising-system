# agents/style_agent.py
"""
Style Improvement Agent
Enhances grammar, readability, and professionalism.
"""

from crewai import Agent, Task


def create_style_agent() -> Agent:
    """
    Create and configure the Style Improvement Agent.
    
    This agent specializes in:
    - Fixing grammar and syntax errors
    - Improving sentence structure and flow
    - Enhancing readability and clarity
    - Adjusting tone and professionalism
    
    Returns:
        Agent: Configured style improvement agent
    """
    return Agent(
        role="Style and Grammar Expert",
        goal=(
            "Improve grammar, sentence structure, readability, professionalism, and overall clarity "
            "to make the response polished and well-written"
        ),
        backstory=(
            "You are a professional writer, editor, and grammarian with expertise in refining written content. "
            "You have an eye for grammar, punctuation, and style. You can identify awkward phrasing, "
            "run-on sentences, and unclear constructions. You improve text by enhancing sentence variety, "
            "ensuring parallel structure, and refining tone to match the audience. "
            "You make responses more engaging, professional, and easy to read. "
            "Your goal is to polish the response until it shines."
        ),
        allow_delegation=False,
        verbose=True,
        tools=[]
    )


def create_style_task(response_text: str, agent: Agent) -> Task:
    """
    Create a style improvement task.
    
    Args:
        response_text (str): The text to improve
        agent (Agent): The style improvement agent
        
    Returns:
        Task: Configured style task
    """
    return Task(
        description=(
            f"Review and improve the following response for grammar, style, and readability. "
            f"Fix all grammatical errors, improve sentence structure, and enhance clarity. "
            f"Ensure the tone is professional and appropriate. "
            f"Improve word choice, enhance transitions between ideas, and refine the overall flow. "
            f"Make the response polished, engaging, and easy to read.\n\n"
            f"Response to polish:\n{response_text}"
        ),
        agent=agent,
        expected_output=(
            "A polished version of the response with improved grammar, sentence structure, and professional tone. "
            "Include notes on the corrections made and improvements to style and readability."
        )
    )
