#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the mock mode functionality directly to verify contact selection.
"""

import sys
import os

def test_mock_mode_contact_selection():
    """Test mock mode contact selection logic"""
    print("🎭 TESTING MOCK MODE CONTACT SELECTION")
    print("=" * 60)
    
    # Import the escalation manager directly
    sys.path.append('app')
    from escalation_manager import EscalationManager
    from agent_tools import AgentDatabaseTools
    
    # Initialize tools
    manager = EscalationManager()
    tools = AgentDatabaseTools()
    
    # Test cases
    test_cases = [
        {
            "name": "Container Incident",
            "query": "Container MSKU7834512 showing duplicate processing in yard management system",
            "expected_contact": "Mark Lee"
        },
        {
            "name": "EDI Incident", 
            "query": "EDI communication failure affecting vessel operations",
            "expected_contact": "Tom Tan"
        },
        {
            "name": "PORTNET Incident",
            "query": "PORTNET system experiencing connection timeouts",
            "expected_contact": "Helpdesk Team"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"🔍 Query: {test_case['query']}")
        
        try:
            # Generate escalation summary using the tools
            summary = tools.generate_escalation_summary(test_case['query'])
            
            # Check if the expected contact is in the summary
            if test_case['expected_contact'] in summary:
                print(f"✅ CORRECT: Found expected contact '{test_case['expected_contact']}'")
            else:
                print(f"❌ WRONG: Expected '{test_case['expected_contact']}' but not found in summary")
                
            # Check for generic contacts (these should NOT appear)
            generic_contacts = ["John Doe", "Jane Smith", "Alex Brown", "Emily White"]
            found_generic = any(contact in summary for contact in generic_contacts)
            
            if found_generic:
                print("❌ PROBLEM: Generic placeholder contacts found in summary!")
                for contact in generic_contacts:
                    if contact in summary:
                        print(f"   - Found: {contact}")
            else:
                print("✅ GOOD: No generic placeholder contacts found")
                
            # Show first few lines of summary
            lines = summary.split('\n')[:8]
            print(f"\n📄 Summary preview:")
            for line in lines:
                if line.strip():
                    print(f"   {line[:80]}{'...' if len(line) > 80 else ''}")
                    
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_mock_mode_contact_selection()
