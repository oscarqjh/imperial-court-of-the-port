"""
Agent tools registration for CrewAI integration.
This module provides a bridge between our database tools and CrewAI agents.
"""

from __future__ import annotations

from typing import Dict, Any, Callable
from .agent_tools import AgentDatabaseTools


def register_agent_tools() -> Dict[str, Callable]:
    """Register database tools for use by CrewAI agents."""
    tools = AgentDatabaseTools()
    
    return {
        # Operational tools
        "get_operational_overview": tools.get_operational_overview,
        "check_system_health": tools.check_system_health,
        
        # Search tools
        "search_containers": tools.search_containers,
        "analyze_edi_messages": tools.analyze_edi_messages,
        "get_vessel_details": tools.get_vessel_details,
        "get_container_details": tools.get_container_details,
        "search_recent_incidents": tools.search_recent_incidents,
        "get_recent_edi_activity": tools.get_recent_edi_activity,
    }


def create_tool_context_for_agents() -> str:
    """Create context string that informs agents about available database tools."""
    return """
AVAILABLE DATABASE TOOLS FOR ANALYSIS:

You have access to the following database tools to retrieve real operational data. 
IMPORTANT: Use these tools to gather factual information before making any analysis or recommendations.

OPERATIONAL OVERVIEW TOOLS:
- get_operational_overview() → Get system baseline (vessel count, container distribution, EDI activity)
- check_system_health() → Current error rates, system stability metrics

SEARCH AND LOOKUP TOOLS:  
- search_containers(container_no=None, status=None, vessel_name=None, port_code=None, limit=10)
- get_container_details(container_no) → Complete container operational status
- get_vessel_details(vessel_name=None, imo_no=None) → Vessel specifications and activity
- analyze_edi_messages(message_type=None, status=None, hours_back=24, limit=20)
- get_recent_edi_activity(limit=10) → Recent EDI message activity

INCIDENT ANALYSIS TOOLS:
- search_recent_incidents(keywords=[], hours_back=48, include_edi_errors=True, include_api_errors=True)

USAGE PROTOCOL:
1. ALWAYS start with get_operational_overview() to understand baseline
2. Use check_system_health() to assess current system state  
3. Search for specific incident-related data using appropriate tools
4. Look for patterns with search_recent_incidents()
5. Base ALL analysis and recommendations on factual data retrieved

Remember: The Imperial Court values decisions based on evidence, not assumptions.
"""
