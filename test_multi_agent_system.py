#!/usr/bin/env python3
"""
Test script for the expanded 6-agent Imperial Court system.
Demonstrates the multi-phase workflow with specialized agents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.orchestrator import ImperialOrchestrator

def test_expanded_agent_system():
    """Test the expanded 6-agent system workflow."""
    print("🏛️ EXPANDED IMPERIAL COURT MULTI-AGENT SYSTEM TEST")
    print("=" * 60)
    
    orchestrator = ImperialOrchestrator()
    
    # Test with a container-related incident
    test_incident = {
        "incident_text": "Container MSKU7890123 showing duplicate discharge status in TOS system causing gate delays and customer complaints. EDI messages showing inconsistent data between COPARN and CODECO messages for this container."
    }
    
    print("📋 TEST INCIDENT:")
    print(f"   {test_incident['incident_text']}")
    print()
    
    if orchestrator.mock_mode:
        print("🎭 RUNNING IN MOCK MODE - Simulating 6-Agent Workflow")
        print()
        print("Expected Agent Workflow:")
        print("1. 察信 (Intelligence) - Evidence gathering from database")
        print("2. 工智 (Technical) - Root cause analysis of container/EDI issue") 
        print("3. 金策 (Business) - Impact on gate operations and customer service")
        print("4. 信儀 (Communication) - Stakeholder notification strategy")
        print("5. 智文 (Strategic) - Synthesis of all specialist analysis")
        print("6. 明鏡 (Validation) - Quality assurance across all domains")
        print("7. 太和智君 (Emperor) - Final escalation summary generation")
        print()
    
    # Run the incident through the system
    result = orchestrator.run(test_incident)
    
    print("📊 ORCHESTRATOR RESULT SUMMARY:")
    print(f"   Emperor: {result.get('emperor', 'Unknown')}")
    print(f"   Incident Type: {result.get('incident_analysis', {}).get('incident_type', 'Unknown')}")
    print(f"   Severity: {result.get('incident_analysis', {}).get('severity', 'Unknown')}")
    print(f"   Database Tools Used: {len(result.get('incident_analysis', {}).get('database_insights_used', []))}")
    print()
    
    if 'escalation_summary' in result:
        print("🎫 ESCALATION SUMMARY GENERATED:")
        print("   ✅ Escalation summary with contact information created")
        print(f"   📞 Contact: {result.get('contact_information', {}).get('name', 'Unknown')}")
        print(f"   🎫 Priority: {result.get('ticket_priority', 'Unknown')}")
        print(f"   🆔 Incident ID: {result.get('incident_id', 'Unknown')}")
        print()
        
        # Show first 500 characters of the escalation summary
        summary = result.get('escalation_summary', '')
        if summary:
            print("📜 ESCALATION SUMMARY PREVIEW:")
            print(summary[:500] + "..." if len(summary) > 500 else summary)
    
    print("\n" + "=" * 60)
    print("🎉 MULTI-AGENT SYSTEM TEST COMPLETED")
    
    return result

if __name__ == "__main__":
    test_expanded_agent_system()
