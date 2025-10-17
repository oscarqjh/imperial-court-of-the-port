from crewai import Agent, Task, Crew, Process
from typing import Optional

class PortIncidentCrew:
    """CrewAI-based system for managing port incidents"""
    
    def __init__(self):
        # Define the incident analyst agent
        self.incident_analyst = Agent(
            role="Port Incident Analyst",
            goal="Analyze port incidents and assess their severity and impact",
            backstory="""You are an experienced port incident analyst with deep knowledge 
            of maritime operations, safety protocols, and emergency response procedures. 
            You excel at quickly assessing situations and providing clear, actionable insights.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Define the response coordinator agent
        self.response_coordinator = Agent(
            role="Emergency Response Coordinator",
            goal="Coordinate appropriate response actions for port incidents",
            backstory="""You are a seasoned emergency response coordinator who specializes 
            in port operations. You have extensive experience in coordinating multi-agency 
            responses and ensuring swift, effective action during incidents.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Define the safety officer agent
        self.safety_officer = Agent(
            role="Port Safety Officer",
            goal="Ensure safety protocols are followed and recommend preventive measures",
            backstory="""You are a dedicated safety officer with comprehensive knowledge 
            of port safety regulations, risk management, and incident prevention. 
            Your primary focus is protecting lives and preventing future incidents.""",
            verbose=True,
            allow_delegation=False
        )
    
    def analyze_incident(self, description: str, severity: Optional[str] = "medium", 
                        location: Optional[str] = None) -> str:
        """
        Analyze a port incident using CrewAI agents
        
        Args:
            description: Description of the incident
            severity: Severity level (low, medium, high, critical)
            location: Location of the incident in the port
            
        Returns:
            Comprehensive analysis and recommendations
        """
        # Create tasks for each agent
        analysis_task = Task(
            description=f"""Analyze the following port incident:
            
            Description: {description}
            Severity Level: {severity}
            Location: {location or 'Not specified'}
            
            Provide a detailed assessment including:
            1. Incident classification
            2. Potential impacts on port operations
            3. Immediate concerns
            4. Risk level evaluation
            """,
            agent=self.incident_analyst,
            expected_output="A detailed incident analysis report"
        )
        
        coordination_task = Task(
            description=f"""Based on the incident analysis, develop a response coordination plan:
            
            Incident: {description}
            Severity: {severity}
            
            Provide:
            1. Immediate response actions
            2. Resources needed
            3. Coordination requirements with relevant authorities
            4. Timeline for response activities
            """,
            agent=self.response_coordinator,
            expected_output="A comprehensive response coordination plan"
        )
        
        safety_task = Task(
            description=f"""Review the incident and response plan from a safety perspective:
            
            Incident: {description}
            Location: {location or 'Not specified'}
            
            Provide:
            1. Safety protocol compliance check
            2. Preventive measures to avoid similar incidents
            3. Safety recommendations for response activities
            4. Long-term safety improvements
            """,
            agent=self.safety_officer,
            expected_output="A detailed safety assessment and recommendations"
        )
        
        # Create and execute the crew
        crew = Crew(
            agents=[self.incident_analyst, self.response_coordinator, self.safety_officer],
            tasks=[analysis_task, coordination_task, safety_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)
