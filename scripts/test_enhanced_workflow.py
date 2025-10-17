#!/usr/bin/env python3
"""
Test the enhanced agent workflow with:
1. Proper escalation paths from contacts.json
2. Historical solution analysis from RAG context
3. 8-agent, 7-phase workflow
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from loguru import logger
from app.orchestrator import ImperialOrchestrator

def test_enhanced_workflow():
    """Test the enhanced 8-agent system with proper escalation and solution analysis."""
    
    logger.info("🧪 TESTING ENHANCED WORKFLOW WITH RAG SOLUTION ANALYSIS AND PROPER ESCALATION")
    logger.info("=" * 80)
    
    # Create orchestrator 
    orchestrator = ImperialOrchestrator()
    
    # Test incident - container duplicate issue
    test_incident = {
        "incident_text": "Duplicate container CMAU0000020 found in system. Container appears in both import and export manifest with conflicting status. Port operations team unable to process vessel discharge due to system conflict. Urgent attention required as vessel PACIFIC STAR waiting at berth."
    }
    
    logger.info("📋 Test Incident:")
    logger.info(f"   {test_incident['incident_text']}")
    logger.info("")
    
    try:
        # Process incident with the enhanced workflow
        result = orchestrator.run(test_incident)
        
        logger.info("✅ ENHANCED WORKFLOW EXECUTION COMPLETED")
        logger.info("=" * 80)
        
        # Analyze results
        logger.info("📊 RESULT ANALYSIS:")
        logger.info(f"   Emperor: {result.get('emperor', 'Unknown')}")
        logger.info(f"   Incident Type: {result.get('incident_analysis', {}).get('incident_type', 'Unknown')}")
        logger.info(f"   Severity: {result.get('incident_analysis', {}).get('severity', 'Unknown')}")
        logger.info(f"   Workflow Phases: {result.get('workflow_phases', 'Unknown')}")
        
        # Check escalation summary
        escalation_summary = result.get('escalation_summary', '')
        if escalation_summary:
            logger.info("   ✅ Escalation summary generated")
            
            # Check for proper contacts from contacts.json
            proper_contacts = [
                'Mark Lee', 'mark.lee@psa123.com',  # Container
                'Tom Tan', 'tom.tan@psa123.com',    # EDI/API
                'Jaden Smith', 'jaden.smith@psa123.com',  # Vessel
                'Jacky Chan', 'jacky.chan@psa123.com'     # Infrastructure
            ]
            
            found_proper_contact = any(contact in escalation_summary for contact in proper_contacts)
            if found_proper_contact:
                logger.info("   ✅ Proper contact from contacts.json found")
            else:
                logger.warning("   ⚠️ No proper contact from contacts.json detected")
                
            # Check for historical solution analysis section
            if 'HISTORICAL SOLUTION' in escalation_summary.upper() or 'SOLUTION ANALYSIS' in escalation_summary.upper():
                logger.info("   ✅ Historical solution analysis included")
            else:
                logger.warning("   ⚠️ Historical solution analysis missing")
                
            # Check for proper escalation path (not fictional contacts)
            bad_contacts = ['Robert Wong', 'Sarah Chen', 'David Liu']
            has_bad_contacts = any(bad_contact in escalation_summary for bad_contact in bad_contacts)
            if not has_bad_contacts:
                logger.info("   ✅ No fictional contacts detected")
            else:
                logger.warning("   ❌ Fictional contacts still present")
                
            # Check for escalation steps from contacts.json
            escalation_keywords = [
                'Product Duty', 'Manager on-call', 'SRE/Infra',  # Container escalation
                'EDI/API team', 'on-call channel',               # EDI escalation
                'Vessel Duty', 'Senior Ops Manager',             # Vessel escalation
                'Infra team'                                     # Infrastructure escalation
            ]
            
            found_escalation_steps = any(keyword in escalation_summary for keyword in escalation_keywords)
            if found_escalation_steps:
                logger.info("   ✅ Proper escalation steps from contacts.json found")
            else:
                logger.warning("   ⚠️ Escalation steps from contacts.json missing")
        else:
            logger.warning("   ❌ No escalation summary generated")
            
        # Display escalation summary excerpt
        if escalation_summary:
            logger.info("")
            logger.info("📋 ESCALATION SUMMARY EXCERPT:")
            logger.info("-" * 60)
            # Show key sections
            lines = escalation_summary.split('\\n')
            
            # Show first 10 lines for incident header
            for i, line in enumerate(lines[:10]):
                logger.info(line.strip())
            
            logger.info("...")
            
            # Look for and show historical solution section
            for i, line in enumerate(lines):
                if 'HISTORICAL SOLUTION' in line.upper() or 'SOLUTION ANALYSIS' in line.upper():
                    # Show this section
                    for j in range(i, min(i + 8, len(lines))):
                        logger.info(lines[j].strip())
                    break
            
            logger.info("...")
            
            # Show escalation path section
            for i, line in enumerate(lines):
                if 'ESCALATION PATH' in line.upper():
                    # Show this section
                    for j in range(i, min(i + 5, len(lines))):
                        logger.info(lines[j].strip())
                    break
            
        # Check RAG context usage
        rag_results = result.get('rag_results', {})
        case_count = rag_results.get('case_history_count', 0)
        kb_count = rag_results.get('knowledge_base_count', 0)
        
        logger.info("")
        logger.info("📚 RAG CONTEXT USAGE:")
        logger.info(f"   Case History Entries: {case_count}")
        logger.info(f"   Knowledge Base Entries: {kb_count}")
        
        if case_count > 0 and kb_count > 0:
            logger.info("   ✅ RAG context successfully retrieved and used")
        else:
            logger.warning("   ⚠️ Limited RAG context available")
            
        logger.info("")
        logger.info("🏁 ENHANCED WORKFLOW TEST COMPLETED")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}")
        return None

if __name__ == "__main__":
    # Set up environment for testing
    os.environ["MOCK_MODE"] = "false"  # Force CrewAI mode to test the enhanced workflow
    
    # Run the test
    test_enhanced_workflow()
