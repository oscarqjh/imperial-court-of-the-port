#!/usr/bin/env python3
"""
Test script to verify that the Imperial Court system correctly uses
the escalation manager to select the appropriate single contact.
"""

from app.orchestrator import ImperialCourtOrchestrator
from app.rag_qdrant import get_relevant_cases, get_relevant_knowledge

def test_container_incident():
    """Test container incident to see if Mark Lee contact is selected"""
    print("🧪 TESTING CONTAINER INCIDENT CONTACT SELECTION")
    print("=" * 60)
    
    incident_text = 'Container MSKU7834512 showing duplicate processing. Operational impact detected in yard management system.'
    
    try:
        court = ImperialCourtOrchestrator()
        cases = get_relevant_cases(incident_text, limit=3) 
        kb = get_relevant_knowledge(incident_text, limit=2)
        
        result = court.run({
            'incident_text': incident_text,
            'rag_context': {'case_history': cases, 'knowledge_base': kb}
        })
        
        print('\n=== ESCALATION SUMMARY ===')
        print(result.get('escalation_summary', 'No escalation summary'))
        
        print('\n=== CONTACT INFORMATION ===') 
        contact = result.get('contact_information', {})
        if contact:
            print(f'Name: {contact.get("name", "N/A")}')
            print(f'Role: {contact.get("role", "N/A")}')
            print(f'Phone: {contact.get("phone", "N/A")}')
            print(f'Email: {contact.get("email", "N/A")}')
            
            # Check if it's the expected contact for container incidents
            if contact.get("name") == "Mark Lee":
                print("\n✅ SUCCESS: Correct contact (Mark Lee) selected for container incident!")
            else:
                print(f"\n❌ ISSUE: Expected Mark Lee, but got {contact.get('name')} for container incident")
        else:
            print('No contact information found')
            
        print(f'\n=== INCIDENT ANALYSIS ===')
        analysis = result.get('incident_analysis', {})
        print(f'Type: {analysis.get("incident_type", "Unknown")}')
        print(f'Severity: {analysis.get("severity", "Unknown")}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

def test_edi_incident():
    """Test EDI incident to see if Sarah Chen contact is selected"""
    print("\n\n🧪 TESTING EDI INCIDENT CONTACT SELECTION")
    print("=" * 60)
    
    incident_text = 'EDI message processing failure. COPARN messages not being received properly from shipping lines.'
    
    try:
        court = ImperialCourtOrchestrator()
        cases = get_relevant_cases(incident_text, limit=3) 
        kb = get_relevant_knowledge(incident_text, limit=2)
        
        result = court.run({
            'incident_text': incident_text,
            'rag_context': {'case_history': cases, 'knowledge_base': kb}
        })
        
        print('\n=== CONTACT INFORMATION ===') 
        contact = result.get('contact_information', {})
        if contact:
            print(f'Name: {contact.get("name", "N/A")}')
            print(f'Role: {contact.get("role", "N/A")}')
            print(f'Phone: {contact.get("phone", "N/A")}')
            print(f'Email: {contact.get("email", "N/A")}')
            
            # Check if it's the expected contact for EDI incidents
            if contact.get("name") == "Sarah Chen":
                print("\n✅ SUCCESS: Correct contact (Sarah Chen) selected for EDI incident!")
            else:
                print(f"\n❌ ISSUE: Expected Sarah Chen, but got {contact.get('name')} for EDI incident")
        else:
            print('No contact information found')
            
        print(f'\n=== INCIDENT ANALYSIS ===')
        analysis = result.get('incident_analysis', {})
        print(f'Type: {analysis.get("incident_type", "Unknown")}')
        print(f'Severity: {analysis.get("severity", "Unknown")}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_container_incident()
    test_edi_incident()
    
    print("\n" + "=" * 60)
    print("🎯 EXPECTED BEHAVIOR:")
    print("- Container incidents → Mark Lee (Container Operations Manager)")
    print("- EDI incidents → Sarah Chen (EDI Systems Manager)")  
    print("- Email incidents → David Kim (IT Support Manager)")
    print("- PORTNET incidents → Lisa Wang (PORTNET Coordinator)")
    print("- General incidents → Alex Johnson (Port Operations Manager)")
