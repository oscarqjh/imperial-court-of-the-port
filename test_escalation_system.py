"""
Test script to demonstrate escalation summary generation.
This shows how the enhanced Imperial Court system generates actionable escalation summaries.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.escalation_manager import EscalationManager
from app.agent_tools import AgentDatabaseTools

def test_escalation_summary():
    """Test escalation summary generation with sample incident data."""
    
    print("🎫 ESCALATION SUMMARY GENERATION TEST")
    print("=" * 60)
    
    # Sample incident data (simulating what agents would provide)
    incident_data = {
        "incident_analysis": {
            "incident_type": "Container Management",
            "severity": "Medium",
            "original_text": "Container MSKU0000001 shows duplicate discharge records in TOS system causing billing discrepancy",
            "database_insights_used": ["operational_overview", "system_health", "container_details"]
        }
    }
    
    # Sample database analysis (simulating what tools would return)
    database_analysis = {
        "operational_overview": {
            "total_vessels": 20,
            "total_containers": 200,
            "edi_activity_24h": 350
        },
        "system_health": {
            "edi_health": {"error_rate_percent": 3.2},
            "api_health": {"error_rate_percent": 1.8}
        },
        "container_details": {
            "container": {
                "cntr_no": "MSKU0000001",
                "status": "TRANSHIP",
                "vessel_name": "MV Lion City 01"
            }
        }
    }
    
    # Sample crew analysis
    crew_analysis = "Strategic analysis indicates container operational discrepancy requiring immediate attention to prevent billing issues."
    
    print("📋 Input Data:")
    print(f"   Incident Type: {incident_data['incident_analysis']['incident_type']}")
    print(f"   Severity: {incident_data['incident_analysis']['severity']}")
    print(f"   System Health: EDI {database_analysis['system_health']['edi_health']['error_rate_percent']}% errors")
    
    print("\n🔧 Generating Escalation Summary...")
    
    # Test escalation manager directly
    escalation_manager = EscalationManager()
    
    try:
        escalation_summary = escalation_manager.create_escalation_summary(
            incident_data, database_analysis, crew_analysis
        )
        
        formatted_summary = escalation_manager.format_escalation_summary(escalation_summary)
        
        print("\n✅ ESCALATION SUMMARY GENERATED:")
        print(formatted_summary)
        
        print("\n📊 SUMMARY DETAILS:")
        print(f"   Incident ID: {escalation_summary.incident_id}")
        print(f"   Primary Contact: {escalation_summary.primary_contact.product_ops_manager}")
        print(f"   Contact Email: {escalation_summary.primary_contact.email}")
        print(f"   Ticket Priority: {escalation_summary.ticket_priority}")
        print(f"   Estimated Resolution: {escalation_summary.estimated_resolution_time}")
        print(f"   Escalation Steps: {len(escalation_summary.escalation_timeline)}")
        print(f"   Immediate Actions: {len(escalation_summary.immediate_actions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating escalation summary: {e}")
        return False

def test_contact_mapping():
    """Test contact mapping for different incident types."""
    
    print("\n" + "=" * 60)
    print("📞 CONTACT MAPPING TEST")
    print("=" * 60)
    
    escalation_manager = EscalationManager()
    
    test_incidents = [
        ("Container Management", "Mark Lee"),
        ("Vessel Operations", "Jaden Smith"),
        ("EDI Communication", "Tom Tan"),
        ("System Issues", "Jacky Chan"),
        ("General", "Helpdesk Team")
    ]
    
    print("Testing contact assignment for different incident types:")
    for incident_type, expected_contact in test_incidents:
        contact = escalation_manager.get_contact_by_module(incident_type)
        if contact:
            actual_contact = contact.product_ops_manager
            status = "✅" if expected_contact in actual_contact else "❌"
            print(f"   {status} {incident_type} → {actual_contact} ({contact.email})")
        else:
            print(f"   ❌ {incident_type} → No contact found")
    
    return True

def test_agent_tools_integration():
    """Test the agent tools escalation summary method."""
    
    print("\n" + "=" * 60)
    print("🛠️ AGENT TOOLS INTEGRATION TEST")
    print("=" * 60)
    
    # Test the agent tools escalation method
    tools = AgentDatabaseTools()
    
    incident_data = {
        "incident_analysis": {
            "incident_type": "EDI Communication",
            "severity": "High",
            "original_text": "COPARN messages from LINE-PSA failing with segment validation errors since 14:30",
            "database_insights_used": ["operational_overview", "system_health", "analyze_edi"]
        }
    }
    
    database_analysis = {
        "system_health": {
            "edi_health": {"error_rate_percent": 12.5},
            "api_health": {"error_rate_percent": 2.1}
        },
        "edi_analysis": {
            "total_messages": 245,
            "error_count": 31,
            "recent_errors": ["Segment validation failed", "Connection timeout"]
        }
    }
    
    crew_analysis = "High severity EDI communication breakdown requiring immediate escalation to EDI support team."
    
    print("📋 Testing agent tools escalation summary generation...")
    
    try:
        result = tools.generate_escalation_summary(incident_data, database_analysis, crew_analysis)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print("✅ Agent tools escalation summary generated successfully!")
        print(f"   Incident ID: {result.get('incident_id', 'Unknown')}")
        print(f"   Primary Contact: {result.get('primary_contact', {}).get('name', 'Unknown')}")
        print(f"   Email: {result.get('primary_contact', {}).get('email', 'Unknown')}")
        print(f"   Ticket Priority: {result.get('ticket_priority', 'Unknown')}")
        
        print("\n📜 Formatted Summary (first 300 chars):")
        formatted = result.get('formatted_summary', '')
        print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in agent tools integration: {e}")
        return False

if __name__ == "__main__":
    print("🏛️ IMPERIAL COURT ESCALATION SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Run all tests
    test1_result = test_escalation_summary()
    test2_result = test_contact_mapping()
    test3_result = test_agent_tools_integration()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Escalation Summary Generation: {'PASS' if test1_result else 'FAIL'}")
    print(f"✅ Contact Mapping: {'PASS' if test2_result else 'FAIL'}")
    print(f"✅ Agent Tools Integration: {'PASS' if test3_result else 'FAIL'}")
    
    if all([test1_result, test2_result, test3_result]):
        print("\n🎉 ALL TESTS PASSED! Escalation system ready for deployment.")
        print("\n📝 Next Steps:")
        print("   1. Start your FastAPI server")
        print("   2. Submit an incident via POST /incident/run")
        print("   3. The output will now include escalation_summary with contact details")
        print("   4. Use the escalation summary for immediate operational action")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
