#!/usr/bin/env python3
"""
Test the new agent-based escalation system where a specialized agent handles 
escalation instead of hard-coded post-processing logic.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from loguru import logger
from app.orchestrator import ImperialOrchestrator

def test_agent_based_escalation():
    """Test the new 7-agent system with dedicated escalation agent."""
    
    logger.info("🧪 TESTING AGENT-BASED ESCALATION SYSTEM")
    logger.info("=" * 60)
    
    # Create orchestrator 
    orchestrator = ImperialOrchestrator()
    
    # Test incident - container duplicate issue
    test_incident = {
        "incident_text": "Duplicate container GESU9876543 found in system. Container appears in both import and export manifest with conflicting status. Port operations team unable to process vessel discharge due to system conflict. Urgent attention required as vessel EVERGREEN GLORY waiting at berth."
    }
    
    logger.info("📋 Test Incident:")
    logger.info(f"   {test_incident['incident_text']}")
    logger.info("")
    
    try:
        # Process incident with the new agent-based system
        result = orchestrator.run(test_incident)
        
        logger.info("✅ ORCHESTRATOR EXECUTION COMPLETED")
        logger.info("=" * 60)
        
        # Analyze results
        logger.info("📊 RESULT ANALYSIS:")
        logger.info(f"   Emperor: {result.get('emperor', 'Unknown')}")
        logger.info(f"   Incident Type: {result.get('incident_analysis', {}).get('incident_type', 'Unknown')}")
        logger.info(f"   Severity: {result.get('incident_analysis', {}).get('severity', 'Unknown')}")
        logger.info(f"   Workflow Phases: {result.get('workflow_phases', 'Unknown')}")
        
        # Check if we have proper escalation summary
        escalation_summary = result.get('escalation_summary', '')
        if escalation_summary and escalation_summary != "Escalation summary generation failed":
            logger.info("   ✅ Escalation summary generated")
            
            # Check for specific contact information (not generic)
            if 'Mark Lee' in escalation_summary or 'Tom Tan' in escalation_summary or '.com' in escalation_summary:
                logger.info("   ✅ Specific contact information found")
            else:
                logger.warning("   ⚠️ Generic or no contact information detected")
                
            # Check for no generic placeholders
            if '[Technical Team Lead Contact Information]' in escalation_summary:
                logger.warning("   ❌ Generic placeholder still present")
            else:
                logger.info("   ✅ No generic placeholders detected")
        else:
            logger.warning("   ❌ No escalation summary generated")
            
        # Display escalation summary excerpt
        if escalation_summary:
            logger.info("")
            logger.info("📋 ESCALATION SUMMARY EXCERPT:")
            logger.info("-" * 40)
            # Show first 500 characters to see contact information
            excerpt = escalation_summary[:500] + "..." if len(escalation_summary) > 500 else escalation_summary
            logger.info(excerpt)
            
        logger.info("")
        logger.info("🏁 AGENT-BASED ESCALATION TEST COMPLETED")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}")
        return None

if __name__ == "__main__":
    # Set up environment for testing
    os.environ["MOCK_MODE"] = "false"  # Force CrewAI mode to test the new agents
    
    # Run the test
    test_agent_based_escalation()
