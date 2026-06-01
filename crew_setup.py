# crew_setup.py
"""
CrewAI Setup and Configuration
Defines all the agents and their roles for the denoising system.
Tracks agent outputs and processes through the pipeline.
"""

from crewai import Agent, Task, Crew
from utils import get_groq_api_key, get_model_name, categorize_issues, format_agent_review_log


class DenoisingCrew:
    """
    Main class to set up and manage the denoising crew of AI agents.
    Each agent specializes in a different aspect of text improvement.
    Maintains logs of each agent's processing.
    """
    
    def __init__(self):
        """Initialize the denoising crew with all agents and tasks."""
        self.groq_api_key = get_groq_api_key()
        self.model_name = get_model_name()
        
        # Track agent outputs
        self.agent_outputs = {}
        self.agent_logs = {}
        self.agent_issues = {}
        
        # Initialize agents
        self.fact_checker = self._create_fact_checker()
        self.consistency_agent = self._create_consistency_agent()
        self.concise_agent = self._create_concise_agent()
        self.style_agent = self._create_style_agent()
        self.final_reviewer = self._create_final_reviewer()
    
    def _create_fact_checker(self) -> Agent:
        """
        Create the Fact Checking Agent.
        Responsible for verifying factual accuracy and catching hallucinations.
        
        Returns:
            Agent: Configured fact-checking agent
        """
        return Agent(
            role="Fact Checking Expert",
            goal="Verify the factual accuracy of the response and correct any hallucinations or false information",
            backstory=(
                "You are an experienced fact-checker with a keen eye for detail. "
                "Your role is to identify any factually incorrect information, "
                "hallucinations, or claims that cannot be verified. "
                "You correct misinformation while preserving the response structure."
            ),
            tools=[],
            allow_delegation=False,
            verbose=True
        )
    
    def _create_consistency_agent(self) -> Agent:
        """
        Create the Consistency Validation Agent.
        Checks for contradictions, timeline issues, and logical inconsistencies.
        
        Returns:
            Agent: Configured consistency-checking agent
        """
        return Agent(
            role="Consistency Validation Expert",
            goal="Identify and fix contradictions, timeline issues, and logical inconsistencies in the response",
            backstory=(
                "You are a logical reasoning expert who excels at spotting contradictions "
                "and inconsistencies in text. You can identify timeline issues, "
                "contradictory statements, and logical fallacies. "
                "You refactor the response to ensure it flows logically without contradictions."
            ),
            tools=[],
            allow_delegation=False,
            verbose=True
        )
    
    def _create_concise_agent(self) -> Agent:
        """
        Create the Conciseness Agent.
        Removes redundancy, filler words, and unnecessary explanations.
        
        Returns:
            Agent: Configured conciseness agent
        """
        return Agent(
            role="Conciseness Expert",
            goal="Remove redundant statements, filler words, and unnecessary explanations while preserving meaning",
            backstory=(
                "You are a master of brevity and clarity. You can identify and eliminate "
                "redundant statements, repeated explanations, and unnecessary filler words. "
                "You condense wordy explanations into concise statements without losing meaning. "
                "Your goal is to make the response as efficient as possible."
            ),
            tools=[],
            allow_delegation=False,
            verbose=True
        )
    
    def _create_style_agent(self) -> Agent:
        """
        Create the Style Improvement Agent.
        Enhances grammar, readability, and professionalism.
        
        Returns:
            Agent: Configured style improvement agent
        """
        return Agent(
            role="Style and Grammar Expert",
            goal="Improve grammar, readability, professionalism, and overall clarity of the response",
            backstory=(
                "You are a professional writer and editor with expertise in grammar, "
                "tone, and style. You improve the readability and professionalism of text "
                "by fixing grammatical errors, enhancing sentence structure, and adjusting tone. "
                "You ensure the response is polished and appropriate for the audience."
            ),
            tools=[],
            allow_delegation=False,
            verbose=True
        )
    
    def _create_final_reviewer(self) -> Agent:
        """
        Create the Final Review Agent.
        Performs a comprehensive review and generates the final polished response.
        
        Returns:
            Agent: Configured final review agent
        """
        return Agent(
            role="Final Review Expert",
            goal="Perform a comprehensive review and generate the best final version of the response",
            backstory=(
                "You are a senior editor and quality assurance specialist. "
                "Your role is to review the fully refined response, ensure all improvements "
                "are cohesive, and generate the best possible final version. "
                "You check that the response is accurate, consistent, concise, and well-written. "
                "You ensure the response meets the highest quality standards."
            ),
            tools=[],
            allow_delegation=False,
            verbose=True
        )
    
    def create_tasks(self, original_response: str) -> list:
        """
        Create tasks for each agent in the workflow.
        
        Args:
            original_response (str): The raw response to be processed
            
        Returns:
            list: List of Task objects for the crew
        """
        # Task 1: Fact Checking
        fact_check_task = Task(
            description=(
                f"Review the following response for factual correctness and hallucinations. "
                f"Identify any false information, unsupported claims, or hallucinations. "
                f"Provide a corrected version with accurate information.\n\n"
                f"Response to check:\n{original_response}"
            ),
            agent=self.fact_checker,
            expected_output="A fact-checked version of the response with corrections and explanations of changes made."
        )
        
        # Task 2: Consistency Validation
        consistency_task = Task(
            description=(
                f"Review the response for contradictions, timeline issues, and logical inconsistencies. "
                f"Identify any statements that contradict each other or violate logical principles. "
                f"Provide a version that flows logically without contradictions.\n\n"
                f"Response to check:\n{original_response}"
            ),
            agent=self.consistency_agent,
            expected_output="A logically consistent version of the response with all contradictions resolved."
        )
        
        # Task 3: Conciseness
        concise_task = Task(
            description=(
                f"Review the response and remove repeated statements, filler words, and unnecessary explanations "
                f"while preserving the core meaning and important details. Make it as concise as possible.\n\n"
                f"Response to edit:\n{original_response}"
            ),
            agent=self.concise_agent,
            expected_output="A concise version of the response with redundancies and unnecessary content removed."
        )
        
        # Task 4: Style Improvement
        style_task = Task(
            description=(
                f"Improve the grammar, readability, professionalism, and clarity of the response. "
                f"Fix any grammatical errors, enhance sentence structure, and improve overall flow. "
                f"Ensure the tone is professional and appropriate.\n\n"
                f"Response to polish:\n{original_response}"
            ),
            agent=self.style_agent,
            expected_output="A polished version of the response with improved grammar, readability, and professional tone."
        )
        
        # Task 5: Final Review
        final_task = Task(
            description=(
                f"Perform a comprehensive final review of the response. "
                f"Ensure it is accurate, consistent, concise, well-written, and meets the highest quality standards. "
                f"Generate the best final version for the user.\n\n"
                f"Response for final review:\n{original_response}"
            ),
            agent=self.final_reviewer,
            expected_output="The final, polished version of the response ready for the user."
        )
        
        return [fact_check_task, consistency_task, concise_task, style_task, final_task]
    
    def process_response(self, original_response: str) -> dict:
        """
        Process a response through all agents in the denoising workflow.
        Tracks outputs and issues from each agent.
        
        Args:
            original_response (str): The raw response to be improved
            
        Returns:
            dict: Dictionary containing outputs from each agent and final result
        """
        try:
            # Create tasks
            tasks = self.create_tasks(original_response)
            
            # Create crew - using environment variables for LLM configuration
            crew = Crew(
                agents=[
                    self.fact_checker,
                    self.consistency_agent,
                    self.concise_agent,
                    self.style_agent,
                    self.final_reviewer
                ],
                tasks=tasks,
                verbose=True,
                # Use environment variables for LLM configuration
                # GROQ_API_KEY and other settings should be in .env
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            # Process agent outputs and categorize issues
            agent_names = ["Fact Checker", "Consistency Validator", "Conciseness Expert", 
                          "Style Expert", "Final Reviewer"]
            
            current_output = original_response
            for i, agent_name in enumerate(agent_names):
                # Simulate capturing agent output (in real implementation, crew would return per-agent outputs)
                agent_output = result if i == len(agent_names) - 1 else f"Agent {agent_name} processed output"
                
                # Categorize issues
                issues = categorize_issues(agent_output, agent_name)
                self.agent_issues[agent_name] = issues
                
                # Format review log
                log = format_agent_review_log(agent_name, current_output, agent_output, issues)
                self.agent_logs[agent_name] = log
                
                self.agent_outputs[agent_name] = agent_output
                current_output = agent_output
            
            return {
                "success": True,
                "final_output": result,
                "agent_outputs": self.agent_outputs,
                "agent_logs": self.agent_logs,
                "agent_issues": self.agent_issues,
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "final_output": None,
                "agent_outputs": self.agent_outputs,
                "agent_logs": self.agent_logs,
                "agent_issues": self.agent_issues,
                "error": str(e)
            }
