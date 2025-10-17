"""
Database tools for AI agents to retrieve operational information.
This module provides structured tools that agents can use to make informed decisions.
"""

from __future__ import annotations

import asyncio
from typing import Dict, Any, List, Optional, Callable
from functools import wraps

from .agents_db import (
    get_vessel_operations_summary,
    search_containers_by_criteria,
    get_edi_message_analysis,
    get_vessel_by_name_or_imo,
    get_container_operational_status,
    get_system_health_metrics,
    search_recent_issues,
    list_recent_edi_messages_orm
)


def sync_wrapper(async_func: Callable) -> Callable:
    """Wrapper to make async functions callable from CrewAI agents."""
    @wraps(async_func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If in async context, we need to use asyncio.create_task
                # But CrewAI typically runs in sync context, so this should work
                return loop.run_until_complete(async_func(*args, **kwargs))
            else:
                return asyncio.run(async_func(*args, **kwargs))
        except Exception as e:
            return {"error": f"Database query failed: {str(e)}"}
    return wrapper


class AgentDatabaseTools:
    """Database tools that AI agents can use to retrieve operational information."""
    
    @staticmethod
    @sync_wrapper
    async def get_operational_overview() -> Dict[str, Any]:
        """
        Get high-level operational overview of port systems.
        
        Use this tool when:
        - Starting incident analysis to understand current system state
        - Need to assess overall port operations capacity
        - Determining resource allocation priorities
        - Understanding baseline system health
        
        Returns summary of vessels, containers, EDI activity, and vessel advice.
        """
        return await get_vessel_operations_summary()
    
    @staticmethod
    @sync_wrapper
    async def check_system_health() -> Dict[str, Any]:
        """
        Get real-time system health metrics and error rates.
        
        Use this tool when:
        - Investigating system performance issues
        - Assessing impact of incidents on operations
        - Need current error rates for EDI and API systems
        - Determining system stability before major operations
        
        Returns EDI/API health metrics, error rates, and operational status.
        """
        return await get_system_health_metrics()
    
    @staticmethod
    @sync_wrapper
    async def search_containers(
        container_no: Optional[str] = None,
        status: Optional[str] = None,
        vessel_name: Optional[str] = None,
        port_code: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for containers by various criteria.
        
        Use this tool when:
        - Investigating container-related incidents
        - Need to find containers by number, status, or vessel
        - Checking container distribution across ports
        - Verifying container operational details
        
        Parameters:
        - container_no: Partial or full container number (supports wildcards)
        - status: Container status (TRANSHIP, IN_YARD, DISCHARGED, etc.)
        - vessel_name: Vessel name (supports partial matching)
        - port_code: Port code (SGSIN, CNSHA, etc.)
        - limit: Maximum number of results (default 10)
        
        Returns list of matching containers with operational details.
        """
        return await search_containers_by_criteria(
            container_no=container_no,
            status=status,
            vessel_name=vessel_name,
            port_code=port_code,
            limit=limit
        )
    
    @staticmethod
    @sync_wrapper
    async def analyze_edi_messages(
        message_type: Optional[str] = None,
        status: Optional[str] = None,
        hours_back: int = 24,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Analyze EDI message patterns and identify issues.
        
        Use this tool when:
        - Investigating EDI communication failures
        - Need to understand message flow patterns
        - Checking for specific message type issues
        - Analyzing EDI system performance over time
        
        Parameters:
        - message_type: EDI message type (COPARN, COARRI, CODECO, IFTMIN)
        - status: Message status (PARSED, ERROR, ACKED)
        - hours_back: How many hours back to analyze (default 24)
        - limit: Maximum messages to retrieve (default 20)
        
        Returns message analysis with error patterns and status distribution.
        """
        return await get_edi_message_analysis(
            message_type=message_type,
            status=status,
            hours_back=hours_back,
            limit=limit
        )
    
    @staticmethod
    @sync_wrapper
    async def get_vessel_details(
        vessel_name: Optional[str] = None,
        imo_no: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific vessel.
        
        Use this tool when:
        - Investigating vessel-specific incidents
        - Need vessel specifications and current status
        - Checking vessel's recent activity and messages
        - Verifying vessel operational details
        
        Parameters:
        - vessel_name: Vessel name (supports partial matching)
        - imo_no: IMO number for exact vessel identification
        
        Returns vessel details with recent activity summary or None if not found.
        """
        return await get_vessel_by_name_or_imo(vessel_name=vessel_name, imo_no=imo_no)
    
    @staticmethod
    @sync_wrapper
    async def get_container_details(container_no: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive operational status of a specific container.
        
        Use this tool when:
        - Investigating container-specific incidents
        - Need complete container operational history
        - Checking container's current status and location
        - Verifying container-related EDI and API activity
        
        Parameters:
        - container_no: Exact container number
        
        Returns container details with vessel info and recent activity or None if not found.
        """
        return await get_container_operational_status(container_no)
    
    @staticmethod
    @sync_wrapper
    async def search_recent_incidents(
        keywords: List[str],
        hours_back: int = 48,
        include_edi_errors: bool = True,
        include_api_errors: bool = True
    ) -> Dict[str, Any]:
        """
        Search for recent system issues and errors by keywords.
        
        Use this tool when:
        - Looking for patterns in recent incidents
        - Investigating recurring issues with specific keywords
        - Need to find similar past incidents for context
        - Checking if current incident is part of larger pattern
        
        Parameters:
        - keywords: List of keywords to search for in error messages
        - hours_back: How many hours back to search (default 48)
        - include_edi_errors: Include EDI error messages (default True)
        - include_api_errors: Include API error events (default True)
        
        Returns recent issues matching keywords with timestamps and details.
        """
        return await search_recent_issues(
            keywords=keywords,
            hours_back=hours_back,
            include_edi_errors=include_edi_errors,
            include_api_errors=include_api_errors
        )
    
    @staticmethod
    @sync_wrapper
    async def get_recent_edi_activity(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent EDI message activity for system monitoring.
        
        Use this tool when:
        - Need quick overview of recent EDI activity
        - Checking latest system communications
        - Monitoring EDI message flow
        - Getting context for EDI-related incidents
        
        Parameters:
        - limit: Number of recent messages to retrieve (default 10)
        
        Returns list of recent EDI messages with status and timing.
        """
        return await list_recent_edi_messages_orm(limit=limit)


# Tool descriptions for agent awareness
AGENT_TOOL_DESCRIPTIONS = {
    "operational_overview": {
        "function": AgentDatabaseTools.get_operational_overview,
        "description": "Get high-level operational overview including vessel count, container status distribution, EDI activity, and vessel advice",
        "when_to_use": "Start of incident analysis, resource allocation decisions, understanding system baseline",
        "example_usage": "tools.get_operational_overview()"
    },
    "system_health": {
        "function": AgentDatabaseTools.check_system_health,
        "description": "Get real-time system health metrics including EDI/API error rates and operational status",
        "when_to_use": "Performance investigations, impact assessment, stability checks",
        "example_usage": "tools.check_system_health()"
    },
    "search_containers": {
        "function": AgentDatabaseTools.search_containers,
        "description": "Search containers by number, status, vessel, or port with flexible criteria",
        "when_to_use": "Container-related incidents, operational verification, status checking",
        "example_usage": "tools.search_containers(status='TRANSHIP', limit=5)"
    },
    "analyze_edi": {
        "function": AgentDatabaseTools.analyze_edi_messages,
        "description": "Analyze EDI message patterns, errors, and performance over time",
        "when_to_use": "EDI communication issues, message flow analysis, system performance",
        "example_usage": "tools.analyze_edi_messages(status='ERROR', hours_back=6)"
    },
    "vessel_details": {
        "function": AgentDatabaseTools.get_vessel_details,
        "description": "Get comprehensive vessel information and recent activity",
        "when_to_use": "Vessel-specific incidents, specifications needed, activity verification",
        "example_usage": "tools.get_vessel_details(vessel_name='MV Lion City')"
    },
    "container_details": {
        "function": AgentDatabaseTools.get_container_details,
        "description": "Get complete operational status and history of specific container",
        "when_to_use": "Container-specific incidents, operational history, status verification",
        "example_usage": "tools.get_container_details('MSKU0000001')"
    },
    "search_incidents": {
        "function": AgentDatabaseTools.search_recent_incidents,
        "description": "Search recent system issues by keywords in error messages",
        "when_to_use": "Pattern analysis, similar incident lookup, recurring issue investigation",
        "example_usage": "tools.search_recent_incidents(['timeout', 'connection'], hours_back=24)"
    },
    "edi_activity": {
        "function": AgentDatabaseTools.get_recent_edi_activity,
        "description": "Get recent EDI message activity for monitoring and context",
        "when_to_use": "EDI monitoring, recent activity context, message flow verification",
        "example_usage": "tools.get_recent_edi_activity(limit=15)"
    }
}


def get_tool_guidance_text() -> str:
    """Generate guidance text for agents about available database tools."""
    guidance = """
DATABASE TOOLS AVAILABLE TO AGENTS:

As an Imperial Court agent, you have access to comprehensive database tools to retrieve operational information. Use these tools strategically to gather relevant data for your analysis and decision-making.

AVAILABLE TOOLS:
"""
    
    for tool_name, info in AGENT_TOOL_DESCRIPTIONS.items():
        guidance += f"""
{tool_name.upper()}:
- Description: {info['description']}
- When to use: {info['when_to_use']}
- Example: {info['example_usage']}
"""
    
    guidance += """
STRATEGIC USAGE GUIDELINES:

1. ALWAYS start major incident analysis with 'operational_overview' to understand baseline
2. Use 'system_health' to assess current system stability and error rates
3. For container-related incidents, use 'search_containers' and 'container_details'
4. For EDI/communication issues, use 'analyze_edi' and 'edi_activity'
5. For vessel-specific problems, use 'vessel_details'
6. Use 'search_incidents' to find similar past issues and patterns
7. Combine multiple tools for comprehensive analysis

THINKING PROCESS:
Before making recommendations, agents should:
1. Assess current system state (operational_overview, system_health)
2. Gather specific incident-related data (search tools)
3. Look for patterns in recent similar incidents
4. Consider operational impact and resource requirements
5. Make informed decisions based on retrieved data

Remember: The database contains real operational data. Use it to ground your analysis in facts rather than assumptions.
"""
    
    return guidance
